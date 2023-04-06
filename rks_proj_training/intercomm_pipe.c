#include <stdio.h>
#include <unistd.h>
#include <string.h>

int main() {
	 int fd1[2], fd2[2], pid;
   	 char message[30];	
   	 if (pipe(fd1) == -1) {
		printf("Pipe1 failed");
		 return 1;
		}

	if (pipe(fd2) == -1) {
		printf("Pipe2 failed");
       		return 1;
    		}

	pid = fork();

	if (pid < 0) {
        	printf("Fork failed");
        	return 1;
    		}
 

    	if (pid > 0) {
        	close(fd1[0]);
        	close(fd2[1]);
        	strcpy(message, "Hello from P1");
        	write(fd1[1], message, 30);
        	close(fd1[1]);
        	read(fd2[0], message, 30);
        	printf("P2 message in P1 side: %s\n", message);
       
   	 } else {
        	close(fd1[1]);
        	close(fd2[0]);
        	read(fd1[0], message, 30);
        	printf("P1 message in P2 side: %s\n", message);
        	strcpy(message, "Hello from P2");
        	write(fd2[1], message, 30);
        	close(fd1[0]);
        	close(fd2[1]);
    		}	
    	
	return 0;
}
