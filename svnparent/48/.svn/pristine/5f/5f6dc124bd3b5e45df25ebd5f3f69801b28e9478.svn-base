/*
 * LCS.cpp
 *
 *  Created on: 19-Mar-2014
 *      Author: Abhimanyu
 */

#include<iostream>
#include<vector>
#include<algorithm>
using namespace std;

void print_graph(vector<vector<vector<string>>>& graph, int ROW_COUNT, int COL_COUNT)
{

}

void longest_common_subsequence(string s_one, string s_two)
{
	vector<vector<vector<string>>> graph(s_one.size(), vector<vector<string>>(s_two.size(),vector<string>(1, "")));
	//graph defined above is a vector, that contains vectors, hence it is a 2-D vector.
	//Each element of this 2-D vector is a vector itself that contains strings. All strings are initialized to null or ""
	//N.o of row is equal to the size of s_one
	//N.o of columns is equal to the size of s-two
	for(size_t i=1; i<s_one.size(); i++)
	{
		for(size_t j=1; j<s_two.size(); j++)
		{
			//The above two nested loops iterate each element (i,j) of the graph
			if(s_one[i] == s_two[j])
			{
				//First case of our algorithm, when s_one's last character is equal to s_two's last character.
				graph[i][j].pop_back(); //Removing the null that was initially inserted
				for(string element:graph[i-1][j-1])
				{
					graph[i][j].push_back(element + s_one[i]);

				}
			}
			else
			{
				//The other case, when they are unequal.
				if(graph[i-1][j][0].size() > graph[i][j-1][0].size())
				{
					graph[i][j].pop_back(); //Removing the null that was initially inserted
					for(string element:graph[i-1][j])
					{
						//checking for all strings in (i-1,j)
						if(find(graph[i][j].begin(), graph[i][j].end(), element) == graph[i][j].end())
						{
							graph[i][j].push_back(element);
						}
					}

				}
				else if(graph[i][j-1][0].size() > graph[i-1][j][0].size())
				{
					graph[i][j].pop_back(); //Removing the null that was initially inserted
					for(string element:graph[i][j-1])
					{
						if(find(graph[i][j].begin(), graph[i][j].end(), element) == graph[i][j].end())
						{
							graph[i][j].push_back(element);
						}
					}

				}
				else if(graph[i-1][j][0]!="" && graph[i][j-1][0]!="") //to avoid pushing "" (null) into the (i,j) vector
				{
					graph[i][j].pop_back(); //Removing the null that was initially inserted
					for(string element:graph[i-1][j])
					{
						graph[i][j].push_back(element);
					}

					for(string element:graph[i][j-1])
					{
						if(find(graph[i][j].begin(), graph[i][j].end(), element) == graph[i][j].end())
						{
							graph[i][j].push_back(element);
						}
					}
				}
			}
		}
	}
	print_graph(graph, s_one.size(), s_two.size());
	cout<<"\n";
	cout<<"LCS is/are : \n";
	for (string element:graph[s_one.size()-1][s_two.size()-1])
	{
		cout<<element<<"\n";
	}

}

int main()
{
	string s_one, s_two;
	cout<<"Enter string 1: \n";
	cin>>s_one;
	cout<<"Enter string 2: \n";
	cin>>s_two;
	string temp = "0";
	s_one = temp + s_one; //appending 0 to the beginning
	s_two = temp + s_two; //appending 0 to the beginning

	longest_common_subsequence(s_one, s_two);

	return 0;
}
