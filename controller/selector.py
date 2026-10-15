def select_server(predictions):
    selected_server = min(
        predictions,
        key=predictions.get
    )

    return selected_server
