// comms.service.ts

import { Injectable } from '@angular/core';
import { Socket } from 'ngx-socket-io';

@Injectable({
  providedIn: 'root'
})
export class CommsService {

  constructor(private socket: Socket) {
    this.connectAndSubscribe();
  }

  private connectAndSubscribe() {
    this.socket.connect();
    this.subscribeToTopic('angular_setup');
  }

  private subscribeToTopic(topic: string) {
    this.socket.on(topic, (message: any) => {
      console.log('Received message:', message);
      // Handle the received message as needed
    });
  }
}
