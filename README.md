# DeepAuc 
Topology:
--------
Network Topology: GEANT2_deep_cache.txt

Simulation code:
---------------

1. Simulation code (C++): GEANT2_deep_cache.cpp (data collection without caching)
                       GEANT2_deep_cache_update.cpp (after implementing caching for preventing congestion and high delay)

- To run GEANT2_deep_cache.cpp and GEANT2_deep_cache_update.cpp (including downloading and compilation instruction), please refer to
http://ndnsim.net.
[ndnSIM documentation](http://ndnsim.net)
                           
2. Deep learning code (Python, keras with tensorflow backend):
Data preparation and cleansing: Data_Preparation3.py (we use traffic_dataset_4_train3.csv for training purpose and traffic_dataset_4_test3.csv for testing purpose)

3. Prediction: Prediction_Traffic3.py (After data preparation and cleansing, we used testing_dataset3.csv for training purpose and training_dataset3.csv for testing purpose).               

- To run Data_Preparation3.py and Prediction_Traffic3.py, please refer to
https://keras.io/ and https://pandas.pydata.org/
[Keras](https://keras.io/)
[Pandas](https://pandas.pydata.org/)

4. Auction code (Julia code):gurobi_vcg_01.jl

- For more information about Julia language, please refer to https://julialang.org/
[Julia documentation](https://julialang.org/)



