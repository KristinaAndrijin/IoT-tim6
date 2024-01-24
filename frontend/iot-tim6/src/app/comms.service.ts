import { Injectable } from '@angular/core';
import { MqttService, IMqttMessage } from 'ngx-mqtt';

@Injectable({
  providedIn: 'root'
})
export class CommsService {

  constructor(private mqttService: MqttService) {}

  connect() {
    this.mqttService.connect();
  }

  subscribeToTopic(topic: string) {
    this.mqttService.observe(topic).subscribe((message: IMqttMessage) => {
      console.log('Received message:', message.payload.toString());
    });
  }
}
