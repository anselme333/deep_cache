# Paper: Joint Deep Learning and Auction for Congestion-based Caching in Named Data Networking
# Author: Anselme
# Interpreter: python 2.7.14 and julia-0.5.2
################
# Needed Packages
using JuMP
using Gurobi
using PyPlot
using StatsBase # Package that provides basic support for statistics
using Distributions
using DataFrames
using CSV
#####################
starting_time= Dates.now()
RANDOM_SEED = 1000
srand(RANDOM_SEED)
# Load prediction data for network optimization and reverse auction
data = CSV.read("C:/Users/anselme/Google Drive/research/Simulation_Research/Journal5/simulation/network_traffic_prediction_final3.csv", nullable=false)
# print(names(data))
size_data_TNP = data[:Kilobytes]
delay = data[:delay]
# We ignored support counts becouse we know InDataName size  in terms of Kilobytes
size_data_ANP = data[:Kilobytes]
f_n_d= zeros(size(size_data_ANP)) # Initiliazation of decision vector to 0
Number_TNP = size(size_data_ANP)
bidding_values = rand(Uniform(2,8), Number_TNP) # Vector of bidding values for contents
consumer_prices = rand(Uniform(6,12), Number_TNP) # Vector of fixed prices for contents
link_capacity = rand(Uniform(563353, 573353), Number_TNP) # Vector of link cacapcity
cache_capacity= rand(Uniform(473353, 573353), Number_TNP) # Vector of cache sizes
delay_threshold = rand(Uniform(2.0, 8.0), Number_TNP) # Vector of delay threshold in termds of ms
cache_price = 0.000003625 # Memory cost 0.003625 per Mb=  0.000003625 per Kb of cache capacity in USD
transit_fee = 0.00063 # transit fee 0.63 usd per Mbps= 0.00063 per 1 Kbps
cache_implementation_cost = cache_price .* cache_capacity
eligible_TNP =  zeros(0)
eligiblle_content_TNP = zeros(0)
eligiblle_content_consumer = zeros(0)
Cache_capacity_TNP = zeros(0)
Cache_capacity_TNP = zeros(0)
link_capacity_TNP = zeros(0)

###############################################################################
# Gurobi
# The problem is infeasible
vcg= Model(solver=GurobiSolver(Presolve=0))
@variable(vcg, x,Bin)
@objective(vcg, Min, sum(bidding_values) * x)
@constraint(vcg, size_data_TNP .* x .<= link_capacity)
@constraint(vcg, sum(x)<=1)
@constraint(vcg, size_data_TNP * x.>= size_data_ANP)
@constraint(vcg, size_data_TNP * x .<= cache_capacity)
@constraint(vcg, delay_threshold * x .<= 10)
@constraint(vcg, bidding_values * x .<= consumer_prices)
println("The optimization problem to be solved (winner encluded) is:")
print(vcg)
status = solve(vcg)
println("Optimal objective: ",getobjectivevalue(vcg),
    ". x = ", getvalue(x))

###############################################################################
# Solve the problem with VCG
i=1
while i <= length(bidding_values)
	# By default delay betha_d= 10 ms
	# Constraint 20e
	if consumer_prices[i] >= bidding_values[i] &&  delay_threshold[i] <=10
	eligible_TNP  = append!(eligible_TNP, bidding_values[i])
	eligiblle_content_TNP =append!(eligiblle_content_TNP, size_data_TNP[i])
	Cache_capacity_TNP =append!(Cache_capacity_TNP, cache_capacity[i])
 link_capacity_TNP =append!(link_capacity_TNP, link_capacity[i])
 eligiblle_content_consumer = append!(eligiblle_content_consumer, consumer_prices[i])

 end
 i += 1
 end

 # Just keep the copy of eligible bidding values and demands

 eligible_bidding_value = abs(eligible_TNP)
 eligible_conten_size = abs(eligiblle_content_TNP)
 total_cache_capaciy_TNP = abs(Cache_capacity_TNP)

 ###############################################################################
# Initialization
# The welfare of other players than TNP n from the chosen outcome
# when TNP n participates in the auction
v_n  = zeros(0)

# The welfare for other bidders than MVNO m from the chosen outcome when TNP
# n is not participating in the auction
v_no_n = zeros(0)

# Winning  bidding values
w = zeros(0)


###############################################################################
# Winner determination algorithm
 # the contraint 20c
while length(eligible_bidding_value) >= 1 && length(eligible_conten_size) >= 1
			 min_bid_value = minimum(eligible_bidding_value)   # Find minimum bidding values
			 k =findfirst(eligible_bidding_value, min_bid_value)
    # Constraint 20a and Constraint 20f
			 if eligible_conten_size[k] <= Cache_capacity_TNP[k] && eligible_conten_size[k] <= link_capacity_TNP[k]
				w=append!(w,  min_bid_value)
				end
				eligible_bidding_value = deleteat!(eligible_bidding_value,k)
				eligible_conten_size = deleteat!(eligible_conten_size,k)
end
# println("winnner value", w)


# just keep a copy of original values
winning_value = abs(w)
winning_value_f = abs(w)
L_bidding_values = abs(eligible_TNP)
L_bidding_demand = abs(eligiblle_content_TNP)
new_winning_values=zeros(0)

###############################################################################
# Price determination algorithm
i=1
while i <= length(winning_value)
	winner_remove = winning_value[i]
	new_min_bid_value = minimum(L_bidding_values)  # Find minimum bidding values
	j =findfirst(L_bidding_values, winner_remove)
	L_bidding_values=deleteat!(L_bidding_values, j)
	L_bidding_demand = deleteat!(L_bidding_demand, j)
	new_winning_values = append!(new_winning_values, new_min_bid_value)
 i += 1
 end
# The chosen outcome when each winning MVNO i is not participating
# println("New winning values  when each winning TNP n is not participating", new_winning_values)



l=1
j=length(new_winning_values)
# Choosen outcome, when each winning MVNO n is not participating
while l <= j
	winnervalue = winning_value[l]
	other_winning_value = new_winning_values[j]
	others_winners_no_n = winning_value[winning_value .≠ winnervalue]
	others_winners_no_n = append!(others_winners_no_n, other_winning_value)
	others_winners_than_n=sum(others_winners_no_n)
	v_no_n = append!(v_no_n, others_winners_than_n)
 l += 1
 end
	# The welfare of other players than MVNO m from the chosen outcome
	# when MVNO m is not participating in auction
# println("Welfare of other players than MVNO m, when m is not there", v_no_n)

# println("winning_value_f", winning_value_f)
i=1
# The chosen outcome when each winning MVNO m is participating in auction
while i <= length(winning_value_f)
	winner_value = winning_value_f[i]
	others_winners_no_n = winning_value_f[winning_value_f .≠ winner_value]
	others_winner2 = sum(others_winners_no_n)
	v_n = append!(v_n, 	others_winner2)
	i += 1
 end
	# The welfare of other players than MVNO m from the chosen outcome
	# when MVNO m participates in auction
# println("Welfare of other players than MVNO n, when m is there", v_n)
# println("length(new_winning_values)", length(new_winning_values))
# println(length(v_no_n))
# println(length(v_n))
social_optimal_price=v_no_n .- v_n
# println("Social optimal price", social_optimal_price)
#  Optiaml Payment

P_optimal = zeros(size(v_n))

#  Auction decision variable

x_decision = zeros(size(v_n))
i = 1
while i <= length(w)
	k = findfirst(eligible_TNP, w[i])
	x_decision[k] = 1  # update decision variables based on the winner
	P_optimal[k] = social_optimal_price[i]
	i += 1
end

# Selecting winner for content delivery
# println("x_decision", x_decision)
selected_winners = eligible_TNP .* x_decision
#println("selected winning bidding values", selected_winners)
# Selecting content sizes
selected_content_sizes = eligiblle_content_TNP .* x_decision

# Payments to TNP for paid contents
payment_content= P_optimal.* x_decision
# println("payments for paid contents", payment_content)
# Payment for transit bandwidth
payment_transit_fee = selected_content_sizes .* transit_fee
# println("Payment for transit bandwidth", payment_transit_fee)

# Total payment for both transit fee and content fee
total_payment_TNPs = payment_content + payment_transit_fee
println("total_payment_TNPs", total_payment_TNPs)

# Payment from consumers
Consumer_payment =  eligiblle_content_consumer .* x_decision
println("Consumer_payment", Consumer_payment)

# cache implementation cost
cache_implementation_payment = selected_content_sizes .* cache_price
println("Consumer_payment", Consumer_payment)

z=[] # Number of customer array Initiliazation
t=[] # ANP profit array Initiliazation
u=[] # TNP profit array Initiliazation
v=[] # CP profit array Initiliazation
numbercostomer = 100 # Number of customer Interested in paid content per day
while numbercostomer<=1000
 Consumer_payment_ANP = 0.15 * (numbercostomer * Consumer_payment)
 Consumer_payment_TNP =0.15  * (numbercostomer * Consumer_payment)
 Consumer_payment_CP =0.70  * (numbercostomer * Consumer_payment)
 ANP_profits = ((Consumer_payment .+ Consumer_payment_ANP) .- cache_implementation_payment) .- total_payment_TNPs
 ANP_profits=sum(ANP_profits)
 TNP_profits = sum(Consumer_payment_TNP.- cache_implementation_payment)
 CP_profits = sum(Consumer_payment_CP.- cache_implementation_payment)
 numbercostomer = numbercostomer + 100
 z=append!(z, numbercostomer)
 t=append!(t, ANP_profits)
 u=append!(u, TNP_profits)
 v=append!(v, CP_profits )
end
len = length(t)
h1 = Vector{Float64}(len)
for i in 2:len
	 h1[i] = mean(t[i-1:i])
 end

 len2 = length(u)
 h2 = Vector{Float64}(len2)
 for i in 2:len2
 	 h2[i] = mean(u[i-1:i])
 end

 len3 = length(v)
 h3 = Vector{Float64}(len3)
 for i in 2:len3
 	h3[i] = mean(v[i-1:i])
 end
# In-Network Caching ISP rofits graph

fig = figure("pyplot_multiaxis")
p = plot(z,h1,color="red",marker="o",markersize=10, linewidth=3.0, label="ANP profit")
p = plot(z,h2,color="purple", marker="*", markersize=20, linewidth=3.0, label="TNP profit")# Plot a basic line
p = plot(z,h3, color="green",linestyle="-",linewidth=3.0, marker="x", markersize=20,label="CP profit") # Plot a basic line
ax = gca()
grid("on")
xlabel("Number of customers", fontsize=18)
font1 = Dict("color"=>"black")
ylabel(" Profit",fontdict=font1, fontsize=18)
setp(ax[:get_yticklabels](),color="black", fontsize=18) # Y Axis font formatting
legend(loc="upper left",fancybox="true", fontsize=18)
ax[:tick_params]("both",labelsize=18)
ax[:ticklabel_format](style="sci",axis="y",scilimits=(0,0))
fig[:canvas][:draw]() # Update the figure
savefig("C:/Users/anselme/Dropbox/Simulation_Research/deep_cache_congestion/Caching_profit.pdf",dpi=95)
gcf() # Needed for IJulia to plot inline
