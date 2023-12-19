try:
    from processor import Processor
except:
    from .processor import Processor


class jsonProcessor(Processor):
    def __init__(self, type):
        super().__init__(type)
