from pgmpy.models import BayesianNetwork
from omegaconf import DictConfig, OmegaConf
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

class PGM:

  # @hydra.main(version_base=None, config_path="conf/pgm", config_name="config")
  def __init__(self, cfg: DictConfig):
    self.cfg = cfg
    self.model = BayesianNetwork(cfg.model.edges)
    self.states =  OmegaConf.to_container(cfg.model.get("states", None))
    cpds = []
    for cpd in cfg.model.cpd:
      state_names = {}
      evidence = cpd.get('evidence', None)
      evidence_card = cpd.get('evidence_card', None)
      if self.states:
        state_names[cpd.variable] = self.states[cpd.variable]
        if evidence:
          state_names.update({e:self.states[e] for e in cpd.evidence})
      
      cpds.append(
        TabularCPD(variable=cpd.variable, variable_card=cpd.cardinality, 
          values=cpd.probabilities, evidence=evidence, evidence_card=evidence_card, state_names=state_names))
    self.model.add_cpds(*cpds)
    assert self.model.check_model() == True
    self.infer = VariableElimination(self.model)

  def print_cpd(self, variable: str):
    print(self.model.get_cpds(variable))

  def predict_dist(self, variables, evidence=None):
    return self.infer.query(variables=variables, evidence=evidence)

  def predict_state(self, variables, evidence=None):
    return self.infer.map_query(variables=variables, evidence=evidence)