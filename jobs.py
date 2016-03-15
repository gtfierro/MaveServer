from mave.core import Preprocessor, ModelAggregator, MnV

def run_mave(filename):
    p0 = Preprocessor(filename)
    m = ModelAggregator(p0)
    model = m.train_hour_weekday()

def run_mnv(filename):
    print MnV(input_file=filename)
