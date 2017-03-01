#include <stdio.h>

int main(){
	
	
	static int c = 5;
	
	printf("%d\n", c);
	
	c++;
	
	{
		c = 50;
	}
	printf("%d\n", c);
	
	//static int c = 55;
	
	printf("%d\n", c);
}