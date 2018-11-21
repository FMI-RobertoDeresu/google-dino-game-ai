config = {
    'mode': 'collect_data',  # collect_data, ai_train, ai_play
    'log_level': 'INFO',
    'train_data': {
        'monitor_number': 1,
        'directory': '../train_data/samples_{datetime}',
        'csv_filename': 'data.csv',
        'image_filename': 'sample_{image_label}_{id}.png'
    }
}