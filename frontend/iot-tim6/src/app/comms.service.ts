import { Injectable } from '@angular/core';
import { Socket } from 'ngx-socket-io';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CommsService {
  private piDevicesSubject: BehaviorSubject<{ [piName: string]: any[] }> = new BehaviorSubject({});
  piDevices$ = this.piDevicesSubject.asObservable();

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

      if (topic === 'angular_setup') {
        this.handleAngularSetupMessage(message);
      }
    });
  }

  private handleAngularSetupMessage(message: any) {
    const piName = message.pi_name;
    const devices = message.devices;

    this.piDevicesSubject.next({ ...this.piDevicesSubject.value, [piName]: devices });
    console.log(this.piDevicesSubject.value);
  }
}
