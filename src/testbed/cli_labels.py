from __future__ import annotations

from octoprobe.util_tentacle_label import label_renderer

from testbed.constants import DIRECTORY_DOWNLOADS
from testbed.tentacles_inventory import TENTACLES_INVENTORY


def main() -> None:
    filename = DIRECTORY_DOWNLOADS / "testbed_labels.pdf"
    label_renderer.create_report(
        filename=filename,
        layout=label_renderer.RendererLabelBolzoneDuo(),
        labels=TENTACLES_INVENTORY.labels_data,
    )
    print(f"Created: {filename}")


if __name__ == "__main__":
    main()
