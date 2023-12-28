# ping_pong_measurer_zenoh_python

---
# How to prepare

Requirements:
- python3
- elipse-zenoh

how to install [elipse-zenoh](https://github.com/eclipse-zenoh/zenoh-python)
```bash
git clone https://github.com/eclipse-zenoh/zenoh-python.git
curl https://sh.rustup.rs -sSf | sh
pip install -r requirements-dev.txt
export PATH="$HOME/.local/bin:$PATH"
maturin build --release
pip install ./target/wheels/<there should only be one .whl file here>
```

# How to Use

In terminal for pong node
```bash
python start_pong_processes.py
```

In terminal for ping node
```bash
python process_measurement_helper.py
```

the data is stored in data folder


