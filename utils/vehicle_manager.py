import glob
import os
import sys
from typing import Sequence
try:
    sys.path.append(glob.glob('carla/PythonAPI/carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla
import hydra
from omegaconf import DictConfig
import time
import logging

from numpy import random
from dataclasses import dataclass
from .common import get_actor_blueprints


class VehicleManager:

    # @hydra.main(config_path="conf", config_name="vehicle_manager")
    def __init__(self, client: carla.Client, asynch: bool, cfg: DictConfig) -> None :
        self.client = client
        self.world = self.client.get_world()
        self.traffic_manager = self.client.get_trafficmanager(cfg.tm_port)
        self.traffic_manager.set_global_distance_to_leading_vehicle(2.5)

        self.car_lights_on = cfg.car_lights_on
        self.hero = cfg.hero
        self.asynch = asynch

        if cfg.respawn:
            self.traffic_manager.set_respawn_dormant_vehicles(True)
        if cfg.hybrid:
            self.traffic_manager.set_hybrid_physics_mode(True)
            self.traffic_manager.set_hybrid_physics_radius(70.0)
        if cfg.seed is not None:
            self.traffic_manager.set_random_device_seed(cfg.seed)
        
        random.seed(cfg.seed if cfg.seed is not None else int(time.time()))
        self.synchronous_master = False

        settings = self.world.get_settings()
        if not self.asynch:
            self.traffic_manager.set_synchronous_mode(True)
            if not settings.synchronous_mode:
                self.synchronous_master = True
                settings.synchronous_mode = True
                settings.fixed_delta_seconds = 0.05
            else:
                self.synchronous_master = False
        else:
            print("You are currently in asynchronous mode. If this is a traffic simulation, \
            you could experience some issues. If it's not working correctly, switch to synchronous \
            mode by using self.traffic_manager.set_synchronous_mode(True)")

        if cfg.no_rendering:
            settings.no_rendering_mode = True
        self.world.apply_settings(settings)

        blueprints = get_actor_blueprints(self.world, cfg.filterv, cfg.generationv)

        if cfg.safe:
            blueprints = [x for x in blueprints if int(x.get_attribute('number_of_wheels')) == 4]
            blueprints = [x for x in blueprints if not x.id.endswith('microlino')]
            blueprints = [x for x in blueprints if not x.id.endswith('carlacola')]
            blueprints = [x for x in blueprints if not x.id.endswith('cybertruck')]
            blueprints = [x for x in blueprints if not x.id.endswith('t2')]
            blueprints = [x for x in blueprints if not x.id.endswith('sprinter')]
            blueprints = [x for x in blueprints if not x.id.endswith('firetruck')]
            blueprints = [x for x in blueprints if not x.id.endswith('ambulance')]

        blueprints = sorted(blueprints, key=lambda bp: bp.id)
        self.blueprints = blueprints

        self.spawn_points = self.world.get_map().get_spawn_points()
        self.vehicles_list = []
        

    
    def spawn_vehicles(self, number_of_vehicles: int) -> Sequence[int]:

        if number_of_vehicles == len(self.vehicles_list):
            print('\nNo change. Number of vehicles: %d' % len(self.vehicles_list))
            return self.vehicles_list
        
        number_of_spawn_points = len(self.spawn_points)
        if number_of_vehicles < number_of_spawn_points:
            random.shuffle(self.spawn_points)
        elif number_of_vehicles > number_of_spawn_points:
            msg = 'requested %d vehicles, but could only find %d spawn points'
            logging.warning(msg, number_of_vehicles, number_of_spawn_points)
            number_of_vehicles = number_of_spawn_points

        # @todo cannot import these directly.
        SpawnActor = carla.command.SpawnActor
        SetAutopilot = carla.command.SetAutopilot
        FutureActor = carla.command.FutureActor
        
        if number_of_vehicles < len(self.vehicles_list):
            num_to_destroy = len(self.vehicles_list) - number_of_vehicles
            print('\nDestroying %d vehicles' % num_to_destroy)
            destroy_list = [self.vehicles_list.pop(random.randint(0, len(self.vehicles_list))) for i in range(num_to_destroy)]
            self.client.apply_batch([carla.command.DestroyActor(x) for x in destroy_list])
            return self.vehicles_list
        else:
            batch = []
            hero = self.hero
            num_to_add = number_of_vehicles - len(self.vehicles_list)
            for n, transform in enumerate(self.spawn_points):
                if n >= num_to_add:
                    break
                blueprint = random.choice(self.blueprints)
                if blueprint.has_attribute('color'):
                    color = random.choice(blueprint.get_attribute('color').recommended_values)
                    blueprint.set_attribute('color', color)
                if blueprint.has_attribute('driver_id'):
                    driver_id = random.choice(blueprint.get_attribute('driver_id').recommended_values)
                    blueprint.set_attribute('driver_id', driver_id)
                if hero:
                    blueprint.set_attribute('role_name', 'hero')
                    self.hero = False
                else:
                    blueprint.set_attribute('role_name', 'autopilot')

                # spawn the cars and set their autopilot and light state all together
                batch.append(SpawnActor(blueprint, transform)
                    .then(SetAutopilot(FutureActor, True, self.traffic_manager.get_port())))

            for response in self.client.apply_batch_sync(batch, self.synchronous_master):
                if response.error:
                    logging.error(response.error)
                else:
                    self.vehicles_list.append(response.actor_id)

            # Set automatic vehicle lights update if specified
            if self.car_lights_on:
                all_vehicle_actors = self.world.get_actors(self.vehicles_list)
                for actor in all_vehicle_actors:
                    self.traffic_manager.update_vehicle_lights(actor, True)

            print('\nAdded %d vehicles' % num_to_add)
            return self.vehicles_list

    def destroy(self):
        if not self.asynch and self.synchronous_master:
            settings = self.world.get_settings()
            settings.synchronous_mode = False
            settings.no_rendering_mode = False
            settings.fixed_delta_seconds = None
            self.world.apply_settings(settings)

        print('\nDestroying %d vehicles' % len(self.vehicles_list))
        self.client.apply_batch([carla.command.DestroyActor(x) for x in self.vehicles_list])