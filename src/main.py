import read_input
import metrics

def main():
    file_path = '../logs.csv'
    csv_reader = read_input.CSVSmallInput()
    data = csv_reader.read(file_path)
    top_5 = metrics.Top5FreqMetric()
    response_time = metrics.ResponseTimeMetric()
    for each_row in data:
        url, action_type = each_row[1], each_row[2] 
        key = (url, action_type)
        top_5.process(key)
        response_time.process(each_row)
    
    for data in top_5.get_result():
        print(data)

    response_time_data = response_time.get_result()
    for uri, value in response_time_data.items():
        print(uri[1], uri[0], value['min_time'],
         value['max_time'], round(value['sum_time']/value['count'], 2))


if __name__ == '__main__':
    main()