import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Vector;

/**
 * 
 */

/**
 * @author zuccong
 *
 */
public class CogeneMatrix {

	
	HashMap<Integer, HashMap<Integer,Double>> fusedCogeneMatrix = new HashMap<Integer, HashMap<Integer,Double>>();
	HashMap<Integer,Double> networkweights = new HashMap<Integer,Double>();
	
	/**
	 * @return the networkweights
	 */
	public HashMap<Integer, Double> getNetworkweights() {
		return networkweights;
	}

	/**
	 * @param networkweights the networkweights to set
	 */
	public void setNetworkweights(HashMap<Integer, Double> networkweights) {
		this.networkweights = networkweights;
	}
	
	public void readNetworkNumberVote(String filePath) throws FileNotFoundException, IOException {
		try (BufferedReader br = new BufferedReader(new FileReader(filePath))) {
			String line;
			while ((line = br.readLine()) != null) {
				String[] networkLine = line.split("\t", -1);
				for(int i = 2; i<networkLine.length;i++) {
					int nodeA = Integer.parseInt(networkLine[i]);
					for(int j = 2; j<networkLine.length;j++) {
						int nodeB = Integer.parseInt(networkLine[j]);
						if(nodeA!=nodeB) {
							HashMap<Integer,Double> tmp = new HashMap<Integer,Double>();
							if(fusedCogeneMatrix.containsKey(nodeA)) {
								tmp = fusedCogeneMatrix.get(nodeA);
								double value =  1.0/6.0;
								if(tmp.containsKey(nodeB))
									value = value + tmp.get(nodeB);
								tmp.put(nodeB, value);
							}else {
								double value =  1.0/6.0;
								tmp.put(nodeB, value);
							}
							fusedCogeneMatrix.put(nodeA, tmp);
						}
					}

				}

			}
		}

	}


	public void readNetworkWeightedVote(String filePath, int networkid) throws FileNotFoundException, IOException {
		try (BufferedReader br = new BufferedReader(new FileReader(filePath))) {
			String line;
			while ((line = br.readLine()) != null) {
				String[] networkLine = line.split("\t", -1);
				for(int i = 2; i<networkLine.length;i++) {
					int nodeA = Integer.parseInt(networkLine[i]);
					for(int j = 2; j<networkLine.length;j++) {
						int nodeB = Integer.parseInt(networkLine[j]);
						if(nodeA!=nodeB) {
							System.out.println(nodeA + " " + nodeB);
							if(nodeA!=nodeB) {
								HashMap<Integer,Double> tmp = new HashMap<Integer,Double>();
								if(fusedCogeneMatrix.containsKey(nodeA)) {
									tmp = fusedCogeneMatrix.get(nodeA);
									double value =  networkWeight(networkid);
									if(tmp.containsKey(nodeB))
										value = value + tmp.get(nodeB);
									tmp.put(nodeB, value);
								}else {
									double value =  networkWeight(networkid);
									tmp.put(nodeB, value);
								}
								fusedCogeneMatrix.put(nodeA, tmp);
							}
						}
					}

				}

			}
		}

	}

	
	public void printCogeneMatrix() {
		Iterator<Entry<Integer, HashMap<Integer, Double>>> it = fusedCogeneMatrix.entrySet().iterator();
	    while (it.hasNext()) {
	        Map.Entry pair = (Map.Entry)it.next();
	        int nodeA = (int) pair.getKey();
	        HashMap<Integer, Double> tmp = (HashMap<Integer, Double>) pair.getValue();
	        Iterator ittmp = tmp.entrySet().iterator();
	        while (ittmp.hasNext()) {
	        	Map.Entry pairtmp = (Map.Entry)ittmp.next();
	        	//System.out.println(nodeA + " " + (int)pairtmp.getKey() + " = " + (double)pairtmp.getValue());
	        }
	    }
	}
	
	public void printCogeneMatrixOnFile(PrintWriter out) {
		Iterator<Entry<Integer, HashMap<Integer, Double>>> it = fusedCogeneMatrix.entrySet().iterator();
	    while (it.hasNext()) {
	        Map.Entry pair = (Map.Entry)it.next();
	        int nodeA = (int) pair.getKey();
	        HashMap<Integer, Double> tmp = (HashMap<Integer, Double>) pair.getValue();
	        Iterator ittmp = tmp.entrySet().iterator();
	        while (ittmp.hasNext()) {
	        	Map.Entry pairtmp = (Map.Entry)ittmp.next();
	        	out.println(nodeA + "\t" + (int)pairtmp.getKey() + "\t" + (double)pairtmp.getValue());
	        }
	    }
    	out.flush();
	}
	
	public double networkWeight(int networkid) {
		switch (networkid) {
		case 1:  return networkweights.get(1);
		case 2:  return networkweights.get(2);
		case 3:  return networkweights.get(3);
		case 4:  return networkweights.get(4);
		case 5:  return networkweights.get(5);
		case 6:  return networkweights.get(6);
		default: return networkweights.get(1);
		}
	}

	
	
	/**
	 * @param args
	 * @throws IOException 
	 * @throws FileNotFoundException 
	 */
	public static void main(String[] args) throws FileNotFoundException, IOException {
		CogeneMatrix cm1 = new CogeneMatrix();
		System.out.println("Reading network");
		
		Vector<String> networkFiles = new Vector<String>();
		for(int i = 0; i < args.length; i++) {
			networkFiles.add(args[i]);
            System.out.println(args[i]);
        }
		for(String file : networkFiles) {
			cm1.readNetworkNumberVote(file);
		}
		
		/*cm1.readNetworkNumberVote("/Users/zuccong/Dropbox/DMI_challenge/results/sc2_round4/run3/1_ppi_anonym_aligned_v2.txt");
		cm1.readNetworkNumberVote("/Users/zuccong/Dropbox/DMI_challenge/results/sc2_round4/run3/2_ppi_anonym_aligned_v2.txt");
		cm1.readNetworkNumberVote("/Users/zuccong/Dropbox/DMI_challenge/results/sc2_round4/run3/3_signal_anonym_aligned_undirected_v3_normalised.txt");
		cm1.readNetworkNumberVote("/Users/zuccong/Dropbox/DMI_challenge/results/sc2_round4/run3/4_coexpr_anonym_aligned_v2.txt");
		cm1.readNetworkNumberVote("/Users/zuccong/Dropbox/DMI_challenge/results/sc2_round4/run3/5_cancer_anonym_aligned_v2.txt");
		cm1.readNetworkNumberVote("/Users/zuccong/Dropbox/DMI_challenge/results/sc2_round4/run3/6_homology_anonym_aligned_v2_normalised.txt");
		*/
		System.out.println("Network read");
		//cm1.printCogeneMatrix();
		PrintWriter out1 = new PrintWriter("../data/subchallenge2/communities_graph_uniform_voting.txt");
		
		cm1.printCogeneMatrixOnFile(out1);
		out1.close();
		
		CogeneMatrix cm2 = new CogeneMatrix();
		
		System.out.println("Reading network");
		cm2.networkweights.put(1, 13.0/52.0);
		cm2.networkweights.put(2, 9.0/52.0);
		cm2.networkweights.put(3, 7.0/52.0);
		cm2.networkweights.put(4, 9.0/52.0);
		cm2.networkweights.put(5, 5.0/52.0);
		cm2.networkweights.put(6, 9.0/52.0);
		
		int i =1;
		for(String file : networkFiles) {
			cm2.readNetworkWeightedVote(file, i);
			i++;
		}
		
		/*
		cm2.readNetworkWeightedVote("/Users/zuccong/Dropbox/DMI_challenge/results/sc2_round4/run3/1_ppi_anonym_aligned_v2.txt", 1);
		cm2.readNetworkWeightedVote("/Users/zuccong/Dropbox/DMI_challenge/results/sc2_round4/run3/2_ppi_anonym_aligned_v2.txt", 2);
		cm2.readNetworkWeightedVote("/Users/zuccong/Dropbox/DMI_challenge/results/sc2_round4/run3/3_signal_anonym_aligned_undirected_v3_normalised.txt", 3);
		cm2.readNetworkWeightedVote("/Users/zuccong/Dropbox/DMI_challenge/results/sc2_round4/run3/4_coexpr_anonym_aligned_v2.txt", 4);
		cm2.readNetworkWeightedVote("/Users/zuccong/Dropbox/DMI_challenge/results/sc2_round4/run3/5_cancer_anonym_aligned_v2.txt", 5);
		cm2.readNetworkWeightedVote("/Users/zuccong/Dropbox/DMI_challenge/results/sc2_round4/run3/6_homology_anonym_aligned_v2_normalised.txt", 6);
		*/
		System.out.println("Network read");
		//cm2.printCogeneMatrix();
		PrintWriter out2 = new PrintWriter("../data/subchallenge2/communities_graph_weighted_voting.txt");
		
		cm2.printCogeneMatrixOnFile(out2);
		out2.close();
		
		
	}

}
