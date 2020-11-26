import abc
import heapq

from collections import defaultdict

class BaseMetric(abc.ABC):
    @abc.abstractmethod
    def process(self, data):
        pass

    @abc.abstractmethod
    def get_result(self):
        pass

class Top5FreqMetric(BaseMetric):
    """Calculate top x values."""
    def __init__(self, size=5):
        self.freq_counter = defaultdict(int)
        self.size = size
        self.result = [0] * size

    def process(self, data):
        # data must be hashable object so that can be counted.
        if not data:
            return
        self.freq_counter[data] += 1
    
    def get_result(self):
        # calculate top x values."""
        freq_heap = []
        for url, freq in self.freq_counter.items():
            key = (freq, url)
            if len(freq_heap) < self.size:
                heapq.heappush(freq_heap, key)
            else:
                min_freq_so_far, _ = freq_heap[0]
                if min_freq_so_far < key[0]:
                    heapq.heappushpop(freq_heap, key)
        
        size = self.size - 1
        while freq_heap:
            self.result[size] = heapq.heappop(freq_heap)
            size -= 1
        return self.result


class ResponseTimeMetric(BaseMetric):
    """Get Max, Min, Average Response time metric from data"""
    def __init__(self):
        self.api_metrics = {}
        

    def process(self, data):
        key = data[1], data[2]
        data[3] = int(data[3])

        if key not in self.api_metrics:
            self.api_metrics[key] = {
                'min_time': data[3],
                'max_time': data[3],
                'sum_time': data[3],
                'count': 1
            }
        else:
            uri_data = self.api_metrics[key]
            if uri_data['min_time'] > data[3]:
                uri_data['min_time'] = data[3]
            elif uri_data['max_time'] < data[3]:
                uri_data['max_time'] = data[3]
            uri_data['sum_time'] += data[3]
            uri_data['count'] += 1



    def get_result(self):
        return self.api_metrics




