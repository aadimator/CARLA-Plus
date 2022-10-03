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

    self.states =  {k: list(cfg.variables[k].states.keys()) for k in cfg.variables.keys()}
    self.variables = {cfg.variables[k].name:k for k in cfg.variables.keys()}

    cpds = []
    for variable in cfg.model.cpd:
      
      cpd = cfg.model.cpd[variable]
      variable_card = len(self.states[variable])
      evidence = cpd.get('evidence', None)
      evidence_card = None

      # To pass onto the CPD function
      state_names = {}
      state_names[variable] = self.states[variable]
      if evidence:
        evidence_card = [len(self.states[e]) for e in evidence]
        state_names.update({e:self.states[e] for e in cpd.evidence})
      
      cpds.append(
        TabularCPD(variable=variable, variable_card=variable_card, 
          values=cpd.probabilities, evidence=evidence, evidence_card=evidence_card, 
          state_names=state_names))

    self.model.add_cpds(*cpds)
    assert self.model.check_model() == True
    self.infer = VariableElimination(self.model)

  def get_states(self):
    states = {self.cfg.variables[k].name: Enum(f'{k}', self.cfg.variables[k].states) 
              for k, in self.states.keys()}
    return SimpleNamespace(**states)

  def get_variables(self):
    return SimpleNamespace(**self.variables)

  def print_cpd(self, variable: str):
    print(self.model.get_cpds(variable))

  def predict_dist(self, variables, evidence=None):
    return self.infer.query(variables=variables, evidence=evidence)

  def predict_state(self, variables, evidence=None):
    return self.infer.map_query(variables=variables, evidence=evidence)