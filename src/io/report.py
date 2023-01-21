from typing import Dict

def write_report(path: str, config: Dict, metrics_values) -> None:
    """ escreve o arquivo de relatorio do experimento """

    report_file = open(path, "w")
    report_file.write(f'dataset: {config["type"]}\n'
                      f'path: {config["train_path"][:config["train_path"].rfind("/") + 1]}\n'
                      f'classifier: {config["classifier"]}\n'
                      f'training time per sample: {metrics_values["training time"]:.3f}s\n'
                      f'inference time per sample: {metrics_values["inference time"]:.3f}s\n'
                      f'accuracy: {metrics_values["accuracy"]:.2f}')