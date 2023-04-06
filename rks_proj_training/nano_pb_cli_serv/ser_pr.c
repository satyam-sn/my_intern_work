#include<stdio.h>
#include<stdlib.h>
#include<sys/types.h>
#include<sys/socket.h>
#include<netinet/in.h>
#include<unistd.h>
#include <pb_encode.h>
#include <pb_decode.h>
#include "simple.pb.h"
int main() {

        
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

	// receiving from server 
	uint8_t buffer[128];
        size_t message_length = recv(sck,buffer,sizeof(buffer),0);
	
	//Decoding the message
        {
                SimpleMessage message = SimpleMessage_init_zero;
		pb_istream_t stream = pb_istream_from_buffer(buffer, message_length);
		pb_decode(&stream, SimpleMessage_fields, &message);

		printf("The decoded message is %d",message.text);
              
         }

//	printf("The decoded message is %d",message.text);
	close(sck);
	close(serv_sock);

	return 0;

}
