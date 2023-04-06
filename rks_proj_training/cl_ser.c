#include<stdio.h>
#include<stdlib.h>
#include<sys/types.h>
#include<sys/socket.h>
#include<netinet/in.h>
#include<unistd.h>
int main() {
	 int pid;
        pid = getppid();
        printf("pid is %d\n",pid);

	
	//create socket
	int nsck;
	nsck = socket(AF_INET,SOCK_STREAM,0);
	
	//assign adrress for socket
	struct sockaddr_in address;
	address.sin_family = AF_INET;
	address.sin_port = htons(9000);
	address.sin_addr.s_addr = INADDR_ANY;
	
	//connect this scoket with address
	int cnt_status = connect(nsck, (struct sockaddr*)&address, sizeof(address));
	if(cnt_status == -1){
		printf("Not connected");
	}

	// sending the message to server
	char clt_message[300] = "This is client ";
	send(nsck,&clt_message,sizeof(clt_message),0);

	
	//receives data from server 
	char message[300];
	recv(nsck, &message,sizeof(message), 0 );
	printf("THe server message is-- %s \n",message);

	// sending the FIN packet
	char msg[10]="FIN";
	printf("The client is sending FIN wating for acknowledgement\n");
	send(nsck,&msg,sizeof(msg),0);
	
	// recieving the packet
	char ms[10];
	recv(nsck,&ms,sizeof(ms),0);
	printf("%s",ms);
//	close(nsck);	
	
	return 0;

}
