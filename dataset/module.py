from typing import Callable, Optional

import pytorch_lightning as pl
from torch.utils.data import DataLoader

from .nanchang import NanchangDataset
from .shanghai import ShanghaiDataset


class DataModule(pl.LightningDataModule):
    def __init__(self, cfg) -> None:
        super(DataModule, self).__init__()
        self.target = cfg["model"]["target"]
        self.cfg = cfg["dataset"]
        self.data_dir = self.cfg["data_dir"]
        self.batch_size = self.cfg["batch_size"]
        self.num_workers = self.cfg["num_workers"]
        self.pin_memory = self.cfg["pin_memory"]
        self.name = self.cfg["name"]
        self.length = self.cfg["length"]

    def setup(self, stage: Optional[str] = None):
        if self.name == "shanghai":
            self.train_dataset = ShanghaiDataset(
                root=self.data_dir, length=self.length["train"], target=self.target
            )
            self.val_dataset = ShanghaiDataset(
                root=self.data_dir, length=self.length["val"], target=self.target
            )
        elif self.name == "nanchang":
            self.train_dataset = NanchangDataset(
                root=self.data_dir, length=self.length["train"], target=self.target
            )
            self.val_dataset = NanchangDataset(
                root=self.data_dir, length=self.length["val"], target=self.target
            )
        else:
            raise ValueError(f"Unknown dataset: {self.name}")

    def train_dataloader(self):
        return DataLoader(
            self.train_dataset,
            batch_size=self.batch_size["train"],  # "train" -> "train"
            num_workers=self.num_workers,
            pin_memory=self.pin_memory,
            shuffle=True,
        )

    def val_dataloader(self):
        return DataLoader(
            self.val_dataset,
            batch_size=self.batch_size["val"],  # "val" -> "val"
            num_workers=self.num_workers,
            pin_memory=self.pin_memory,
            shuffle=False,
        )
