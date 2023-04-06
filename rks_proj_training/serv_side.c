#include<stdio.h>
#include<stdlib.h>
#include<sys/types.h>
#include<sys/socket.h>
#include<netinet/in.h>
#include<time.h>
#include<sys/signal.h>
#include<unistd.h>
int main() {
	
	int pid;
	pid = getppid();
	printf("pid is %d",pid);
	char ser_messg[300] = "This is server";
	
	// CREATE SRVER SOCKET
	int serv_sock;
	serv_sock = socket(AF_INET, SOCK_STREAM, 0);
	
	// SERVER ADDRESS
	struct sockaddr_in addr;
 	addr.sin_family = AF_INET;
        addr.sin_port = htons(9000);
        addr.sin_addr.s_addr = INADDR_ANY;
	
	// bind this server to our addr and port
	bind(serv_sock, (struct sockaddr*)&addr, sizeof(addr));

	//listen for the request
	listen(serv_sock,5);
	
	//accepting the coonection from client
	int sck;
	sck = accept(serv_sock,NULL,NULL);

	// receiving from client 
	char  clt_mesg[300];
	recv(sck, &clt_mesg, sizeof(clt_mesg),0);
	printf("The message from client is %s\n", clt_mesg);
	
	// sending to client 
	send(sck, ser_messg, sizeof(ser_messg), 0);
	
	//sending acknowledgement to client
	char msg[10];
	recv(sck, &msg, sizeof(msg), 0);
	printf("%s\n",msg);
	
	if( strcmp(msg, "FIN") == 0){
		
		printf("Recieved FIN now sending ACK");
			
		
	char ms[10]="ACK";
	 
	send(sck, ms, sizeof(msg),0);
	}
	sleep(20);
	kill(29076,9);
	close(sck);	
	close(serv_sock);
	
	return 0;
}

