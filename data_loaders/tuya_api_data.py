from mage_ai.data_preparation.shared.secrets import get_secret_value
import tinytuya

@data_loader
def load_data_from_api(*args, **kwargs):

    tuya_cloud = tinytuya.Cloud(
                    apiRegion = get_secret_value('tuya_api_endpoint'),
                    apiKey = get_secret_value('tuya_access_id'),
                    apiSecret =  get_secret_value('tuya_access_key'))

    # Create an empty list to receive all data from the devices
    all_data_devices = []

    # Get information about all devices in Tuya
    devices = tuya_cloud.getdevices()

    # Get a list with only name and id of each device
    list_devices = [(device['name'], device['id']) for device in devices]

    # Extract power and timestamp for each connected device of the list
    for device in list_devices:
        if tuya_cloud.getconnectstatus(device[1]): # If it is not connected it is ignored
            status_device = tuya_cloud.getstatus(device[1]) # Get information based on id
            all_data_devices.append({'device_uid': device[1], 'name': device[0], 'status_device': status_device})

    return all_data_devices