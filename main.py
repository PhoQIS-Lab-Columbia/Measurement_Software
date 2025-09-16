from Instruments.network_manager import NetworkManager
nm = NetworkManager()
vna = nm.connect_vector_network_analyzer()
print(vna.get_id())