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
    this.subscribeToTopic('values');
  }

  private subscribeToTopic(topic: string) {
    this.socket.on(topic, (message: any) => {
      //console.log('Received message:', message);

      if (topic === 'angular_setup') {
        this.handleAngularSetupMessage(message);
      }

      if (topic === 'values') {
        this.updateDeviceValues(message);
      }
    });
  }

  private handleAngularSetupMessage(message: any) {
    const piName = message.pi_name;
    console.log(piName)
    const devices = message.devices;
    console.log(devices)

    this.piDevicesSubject.next({ ...this.piDevicesSubject.value, [piName]: devices });
    console.log(this.piDevicesSubject.value);
  }


  private updateDeviceValues(message: any) {
    const piName = message.code;
    const measurement = message.measurement;
    const value = message.value;
    let lmao = {"measurement":measurement,"value":value}
    //console.log("devices")
    //console.log(devices)
   

    this.piDevicesSubject.next({ ...this.piDevicesSubject.value, [piName]: lmao });
    console.log(this.piDevicesSubject.value);
  }

}


