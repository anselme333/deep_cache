# DeepAuc 

We summarize the connection between all components of DeepAu and all procedures for utilizing our source code available as follows:
 First, in ndnSIM, we used GEANT2 deep cache.cpp and GEANT2 deep cache topology.txt for collecting dataset. We run GEANT2 deep cache.cpp two times (for a period of 4 hours) for collecting training and testing datasets. Then, we save the collected datasets in rate trace GEANT2 myproposal.txt files. 
 Second, we perform data cleaning by removing unwanted features such as face description and type. Then, we save the outputs in .csv format (traffic dataset 4 train3.csv, traffic dataset 4 test3.csv).
 Third, we map the collected dataset with topology for getting connecting between nodes, bandwidth, metric, delay, and queue. Then, we identify the content names that pass through outgoing and incoming faces of transit links. The Python source codes for data preparation are available in Data Preparation3.py. We save the output of data preparation in .csv format (training dataset3.csv and testing dataset3.csv). 
 Fourth, we feed the cleaned and prepared datasets in LSTM model, where we use training dataset3.csv for the training dataset and testing dataset3.csv for testing dataset. Then, we predict the future demands for contents need to pass through the transit links, where the output of our prediction is saved in network traffic prediction3.csv. The python source codes of our prediction are available in Prediction Traffic3.py
 Firth, thus, we use 20 time slots for window size or loopback values which cause our prediction approach to start having predicted transit traffic from 21st time slot, we removed the rows that have missing predicted transit traffic (the first 20 time slots). Then, we save the final result in network traffic prediction3.csv.
 Sixth, we feed the prediction output (network traffic prediction3.csv) in our auction codes and generated randomly the bidding values for purchasing the contents that have high predicted future demands and need to pass through the transit links. The Julia source codes for our auction are available in gurobi vcg 01.jl.
 Finally, to cache the purchased contents that have high predicted future demands and need to pass through the transit links, we update GEANT2 deep cache.cpp and implement cache storage in ndnSIM for preventing congestion and minimizing transit bandwidth consumption. The source codes for implementing cache storage in ndnSIM is available in GEANT2 deep cache update.

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



