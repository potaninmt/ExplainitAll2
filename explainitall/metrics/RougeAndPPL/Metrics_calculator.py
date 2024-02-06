class Metrics_calculator:
    
    # CONSTRUCTOR / DESTRUCTOR:
    
    def __init__(self, tokenizer):
        self.metrics_ = {}
        self.preprocessing_functions_ = {}
        self.tokenizer_ = tokenizer
        
    def __del__(self):
        del self.metrics_
        del self.tokenizer_
        
    # FUNCTIONS:
    
    def calculate(self, contexts, references, candidates):
        res = {}

        assert len(contexts) == len(references), "length of candidates not equal to length of references"
        assert len(references) == len(candidates), "length of candidates not equal to length of references"

        preprocessed_sentences = {}
        for preproc in self.preprocessing_functions_:
            preprocessed = preproc(contexts, references, candidates, self.tokenizer_)
            preprocessed_sentences[frozenset(self.preprocessing_functions_[preproc])] = preprocessed

        for metric_name in self.metrics_:
            for metric_group in preprocessed_sentences:
                if metric_name in metric_group:
                    prep = preprocessed_sentences[metric_group]
                    prep_references = prep['references']
                    prep_candidates = prep['candidates']
                    res[metric_name] = self.metrics_[metric_name].calculate(prep_references, prep_candidates)
                    break

        '''
        references_encodings = self.tokenizer_(references)
        candidates_encodings = self.tokenizer_(candidates)
        
        for metric_name in self.metrics_:
            res[metric_name] = self.metrics_[metric_name].calculate(references_encodings.input_ids, candidates_encodings.input_ids)
        '''
                
        return res
    
    def add_metric(self, name, metric):
        if name in self.metrics_:
            raise Exception('Metric name ' + name + ' already exists!')
        self.metrics_[name] = metric

        preproc = metric.preprocess
        if preproc not in self.preprocessing_functions_:
            self.preprocessing_functions_[preproc] = set()
        self.preprocessing_functions_[preproc].add(name)
            
    # FIELDS:
    
    metrics_ = None
    preprocessing_functions_ = None
    tokenizer_ = None
