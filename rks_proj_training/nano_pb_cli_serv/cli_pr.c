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

        

	 // This is the buffer where we will store our message and encode our message. 
   	uint8_t buffer[128];
    	size_t message_length;

    	{	
        	SimpleMessage message = SimpleMessage_init_zero;

        	pb_ostream_t stream = pb_ostream_from_buffer(buffer, sizeof(buffer));
        	message.text =20;
        	pb_encode(&stream, SimpleMessage_fields, &message);
        	message_length = stream.bytes_written;
	
		// Sending the encoded meesage 
		printf("Sending the encoded message to server that is :%d\n",message.text);
        	send(nsck,buffer,message_length,0);
		
    	}	
        
	close(nsck);

	return 0;
}
