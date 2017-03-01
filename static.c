#include <stdio.h>

int main(){
	
	
	static int c = 5;
	
	printf("%d", c);
	
	c++;
	
	printf("%d", c);
	
	//static int c = 55;
	
	printf("%d", c);
}