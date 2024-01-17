# ping_pong_measurer_zenoh_python

# How to prepare

Requirements:
- python >= 3.9
- elipse-zenoh

please follow [how to install elipse-zenoh](https://github.com/eclipse-zenoh/zenoh-python)

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
python src/start_pong_processes.py --node 5
```
5 pong nodes are running

In terminal for ping node
```bash
python src/process_measurement_helper.py --node 5 --mt 1 --pt 1 --pb 100 
```
5 ping nodes are running and start ping-pong communication with pong nodes.
In this case, the number of measurement (--mt) is 1, the number of pingpong (-pt) is 1, and the payload byte (--pb) is 100.

the data is stored in csv format in ./data


