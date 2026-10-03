import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from local_simulator.runtime_loader import install_bundled_pyphysx
install_bundled_pyphysx()
import pyphysx
print([name for name in dir(pyphysx) if any(key in name.lower() for key in ('solve','replay','scalar','friction','integrate'))])
