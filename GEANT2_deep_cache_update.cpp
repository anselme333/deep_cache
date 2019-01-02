/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */
/**
* Copyright (c) 2011-2015  Regents of the University of California.
*
* This file is part of ndnSIM. See AUTHORS for complete list of ndnSIM authors and
* contributors.
*
* ndnSIM is free software: you can redistribute it and/or modify it under the terms
* of the GNU General Public License as published by the Free Software Foundation,
* either version 3 of the License, or (at your option) any later version.
*
* ndnSIM is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
* without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
* PURPOSE.  See the GNU General Public License for more details.
*
* You should have received a copy of the GNU General Public License along with
* ndnSIM, e.g., in COPYING.md file.  If not, see <http://www.gnu.org/licenses/>.
**/
// congestioncontrolsenario2.cpp

#include <memory>
#include "ns3/ptr.h"
#include "ns3/log.h"
#include "ns3/command-line.h"
#include <list>
#include <vector>
#include "ns3/queue.h"
#include "ns3/config.h"
#include "ns3/uinteger.h"
#include "ns3/string.h"
#include "ns3/drop-tail-queue.h"
#include "ns3/node.h"
#include "ns3/packet.h"
#include "ns3/core-module.h"
#include "ns3/ndnSIM-module.h"
#include "ns3/network-module.h"
#include "ns3/flow-monitor-helper.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"
#include "ns3/traced-callback.h"
#include "ns3/ndnSIM/model/ndn-common.hpp"
#include "ns3/point-to-point-net-device.h"
#include "ns3/ndnSIM/NFD/daemon/face/face.hpp"
#include "ns3/ndnSIM/model/ndn-l3-protocol.hpp"

namespace ns3 {
int main(int argc, char* argv[])
{
CommandLine cmd;
cmd.Parse (argc, argv);
cmd.Parse(argc, argv);

AnnotatedTopologyReader topologyReader("", 25);
topologyReader.SetFileName("src/ndnSIM/examples/topologies/GEANT2_deep_cache.txt");
topologyReader.Read();

// Install NDN stack on all nodes
ndn::StackHelper ndnHelper;
ndnHelper.SetDefaultRoutes(true);

// Getting containers for the consumer/producer
Ptr<Node> consumer1 = Names::Find<Node>("Src1");
Ptr<Node> consumer2 = Names::Find<Node>("Src2");
Ptr<Node> consumer3 = Names::Find<Node>("Src3");
Ptr<Node> consumer4 = Names::Find<Node>("Src4");
Ptr<Node> consumer5 = Names::Find<Node>("Src5");
Ptr<Node> consumer6 = Names::Find<Node>("Src6");
Ptr<Node> consumer7 = Names::Find<Node>("Src7");
Ptr<Node> consumer8 = Names::Find<Node>("Src8");
Ptr<Node> consumer9 = Names::Find<Node>("Src9");
Ptr<Node> consumer10 = Names::Find<Node>("Src10");
Ptr<Node> consumer11 = Names::Find<Node>("Src11");
Ptr<Node> consumer12 = Names::Find<Node>("Src12");
Ptr<Node> consumer13 = Names::Find<Node>("Src13");
Ptr<Node> consumer14 = Names::Find<Node>("Src14");
Ptr<Node> consumer15 = Names::Find<Node>("Src15");
Ptr<Node> consumer16 = Names::Find<Node>("Src16");
Ptr<Node> consumer17 = Names::Find<Node>("Src17");
Ptr<Node> consumer18 = Names::Find<Node>("Src18");
Ptr<Node> consumer19 = Names::Find<Node>("Src19");
Ptr<Node> consumer20 = Names::Find<Node>("Src20");
Ptr<Node> GR1= Names::Find<Node>("R1");
Ptr<Node> GR2= Names::Find<Node>("R2");
Ptr<Node> GR3= Names::Find<Node>("R3");
Ptr<Node> GR4= Names::Find<Node>("R4");
Ptr<Node> GR5= Names::Find<Node>("R5");
Ptr<Node> GR6= Names::Find<Node>("R6");
Ptr<Node> GR7= Names::Find<Node>("R7");
Ptr<Node> GR8= Names::Find<Node>("R8");
Ptr<Node> GR9= Names::Find<Node>("R9");
Ptr<Node> GR10= Names::Find<Node>("R10");
Ptr<Node> GR11= Names::Find<Node>("R11");
Ptr<Node> GR12= Names::Find<Node>("R12");
Ptr<Node> GR13= Names::Find<Node>("R13");
Ptr<Node> GR14= Names::Find<Node>("R14");
Ptr<Node> GR15= Names::Find<Node>("R15");
Ptr<Node> GR16= Names::Find<Node>("R16");
Ptr<Node> GR17= Names::Find<Node>("R17");
Ptr<Node> GR18= Names::Find<Node>("R18");
Ptr<Node> GR19= Names::Find<Node>("R19");
Ptr<Node> GR20= Names::Find<Node>("R20");
Ptr<Node> GR21= Names::Find<Node>("R21");
Ptr<Node> GR22= Names::Find<Node>("R22");
Ptr<Node> GR23= Names::Find<Node>("R23");
Ptr<Node> cp1 = Names::Find<Node>("CP1");



// We need large cache sizes on congested links
// Cache replacemnet polocity: Last Recently Used (LRU)
ndnHelper.SetOldContentStore ("ns3::ndn::cs::Stats::Lru","MaxSize", "1000000");
ndnHelper.Install(GR1);
ndnHelper.Install(GR2);
ndnHelper.Install(GR3);
ndnHelper.Install(GR6);
ndnHelper.Install(GR7);
ndnHelper.Install(GR9);
ndnHelper.Install(GR10);
ndnHelper.Install(GR12);
ndnHelper.Install(GR22);
ndnHelper.Install(GR23);

// We need small cache sizes on non-congested links
ndnHelper.SetOldContentStore ("ns3::ndn::cs::Stats::Lru","MaxSize", "100000");
ndnHelper.Install(GR4);
ndnHelper.Install(GR5);
ndnHelper.Install(GR8);
ndnHelper.Install(GR11);
ndnHelper.Install(GR13);
ndnHelper.Install(GR14);
ndnHelper.Install(GR15);
ndnHelper.Install(GR16);
ndnHelper.Install(GR17);
ndnHelper.Install(GR18);
ndnHelper.Install(GR19);
ndnHelper.Install(GR20);
ndnHelper.Install(GR21);


//cache storage is not needed for CP
ndnHelper.SetOldContentStore("ns3::ndn::cs::Nocache");
ndnHelper.Install(cp1);

//Cache storages are not needed for Consumers
ndnHelper.SetOldContentStore("ns3::ndn::cs::Nocache");
ndnHelper.Install(consumer1);
ndnHelper.Install(consumer2);
ndnHelper.Install(consumer3);
ndnHelper.Install(consumer4);
ndnHelper.Install(consumer5);
ndnHelper.Install(consumer6);
ndnHelper.Install(consumer7);
ndnHelper.Install(consumer8);
ndnHelper.Install(consumer9);
ndnHelper.Install(consumer10);
ndnHelper.Install(consumer11);
ndnHelper.Install(consumer12);
ndnHelper.Install(consumer13);
ndnHelper.Install(consumer14);
ndnHelper.Install(consumer15);
ndnHelper.Install(consumer16);
ndnHelper.Install(consumer17);
ndnHelper.Install(consumer18);
ndnHelper.Install(consumer19);
ndnHelper.Install(consumer20);

// Choosing forwarding strategy

ndn::StrategyChoiceHelper::InstallAll("/com/news", "/localhost/nfd/strategy/multicast");
ndn::StrategyChoiceHelper::InstallAll("/com/video", "/localhost/nfd/strategy/multicast");
ndn::StrategyChoiceHelper::InstallAll("/com/ccn", "/localhost/nfd/strategy/multicast");

// install application helper

ndn::AppHelper consumerHelper1("ns3::ndn::ConsumerCbr");
consumerHelper1.SetAttribute("Frequency", StringValue("300")); // 300 interests a second
ndn::AppHelper consumerHelper2("ns3::ndn::ConsumerCbr");
consumerHelper2.SetAttribute("Frequency", StringValue("300")); // 300 interests a second
ndn::AppHelper consumerHelper3("ns3::ndn::ConsumerCbr");
consumerHelper3.SetAttribute("Frequency", StringValue("300")); // 300 interests a second


// that will express interests in /com/video namespace

consumerHelper1.SetPrefix("/com/video");
consumerHelper1.Install(consumer1);
consumerHelper1.Install(consumer2);
consumerHelper1.Install(consumer3);
consumerHelper1.Install(consumer4);
consumerHelper1.Install(consumer5);
consumerHelper1.Install(consumer6);
consumerHelper1.Install(consumer7);
consumerHelper2.SetPrefix("/com/news");
consumerHelper2.Install(consumer8);
consumerHelper2.Install(consumer9);
consumerHelper2.Install(consumer10);
consumerHelper2.Install(consumer11);
consumerHelper2.Install(consumer12);
consumerHelper2.Install(consumer13);
consumerHelper2.Install(consumer14);
consumerHelper3.SetPrefix("/com/ccn");
consumerHelper3.Install(consumer15);
consumerHelper3.Install(consumer16);
consumerHelper3.Install(consumer17);
consumerHelper3.Install(consumer19);
consumerHelper3.Install(consumer20);

ndn::AppHelper producerHelper1("ns3::ndn::Producer");
producerHelper1.SetAttribute("PayloadSize", StringValue("1024"));
ndn::AppHelper producerHelper2("ns3::ndn::Producer");
producerHelper2.SetAttribute("PayloadSize", StringValue("1024"));
ndn::AppHelper producerHelper3("ns3::ndn::Producer");
producerHelper3.SetAttribute("PayloadSize", StringValue("1024"));
producerHelper1.SetPrefix("/com/video");
producerHelper2.SetPrefix("/com/news");
producerHelper3.SetPrefix("/com/ccn");
producerHelper1.Install(cp1);
producerHelper2.Install(cp1);
producerHelper3.Install(cp1);


// Collect traffic information

// Drop tracer
L2RateTracer::InstallAll("drop-trace_GEANT2_myproposal.txt", Seconds(1));
// Rate tracer
ndn::L3RateTracer::InstallAll("rate-trace_GEANT2_myproposal.txt", Seconds(1));
// Delay Rate tracer
ndn::AppDelayTracer::InstallAll("Delay-trace_GEANT2_myproposal.txt");
// Delay CS
ndn::CsTracer::InstallAll("cs-trace_GEANT2_myproposal.txt", Seconds(1));
//Running time
Simulator::Stop(Seconds(14400)); // 14400 seconds= 4 hours
Simulator::Run();

return 0;
}

} // namespace ns3

int
main(int argc, char* argv[])
{
return ns3::main(argc, argv);

}
