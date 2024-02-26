# Export data into a .csv file
def save_to_csv(data, filename):
    with open(os.path.join(pwd, server_app_folder, filename), 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = data[0][0].keys()  # Assuming the data is not empty
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for record in data:
            for item in record:
                writer.writerow(item)

# Sort a list of logs names
def sort_list_logs(logs):
    def logs_modifications(log):
        # remove the '-' from the log
        date_part, number_part = log.split('-')[:3], log.split('-')[3]
        # Join the parts of date to transform
        date_log = '-'.join(date_part)
        # remove the '.log' extension and pass the number to int
        number_log = int(number_part.split('.')[0])
        # return the date and number for sorting
        return date_log, number_log

    # use the logs_modifications function to sort the logs by date and number
    sorted_logs = sorted(logs, key=logs_modifications)
    return sorted_logs

# Flatten a list with lists inside
def flatten_list(list_of_lists):
  flat_list = []
  for sublist in list_of_lists:
    for element in sublist:
      flat_list.append(element)
  return flat_list