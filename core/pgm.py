from enum import Enum
from types import SimpleNamespace
from pgmpy.models import BayesianNetwork
from omegaconf import DictConfig, OmegaConf
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

class PGM:

  # @hydra.main(version_base=None, config_path="conf/pgm", config_name="config")
  def __init__(self, cfg: DictConfig):
    self.cfg = cfg
    self.model = BayesianNetwork(cfg.model.edges)
    self.states =  cfg.model.get("states", None)
    if self.states:
      self.states = OmegaConf.to_container(self.states)
    
    cpds = []
    for variable in cfg.model.cpd:
      state_names = {}
      cpd = cfg.model.cpd[variable]
      evidence = cpd.get('evidence', None)
      evidence_card = None
      if evidence:
        evidence_card = [cfg.model.cpd[e].cardinality for e in evidence]
      if self.states:
        state_names[variable] = self.states[variable]
        if evidence:
          state_names.update({e:self.states[e] for e in cpd.evidence})
      
      cpds.append(
        TabularCPD(variable=variable, variable_card=cpd.cardinality, 
          values=cpd.probabilities, evidence=evidence, evidence_card=evidence_card, state_names=state_names))

    self.model.add_cpds(*cpds)
    assert self.model.check_model() == True
    self.infer = VariableElimination(self.model)

  def get_states(self):
    states = {self.cfg.model.cpd[k].name: Enum(f'{k}', self.states[k]) for k, v in self.states.items()}
    return SimpleNamespace(**states)

  def print_cpd(self, variable: str):
    print(self.model.get_cpds(variable))

  def predict_dist(self, variables, evidence=None):
    return self.infer.query(variables=variables, evidence=evidence)

  def predict_state(self, variables, evidence=None):
    return self.infer.map_query(variables=variables, evidence=evidence)