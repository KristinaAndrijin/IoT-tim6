import { Injectable } from '@angular/core';
import { Socket } from 'ngx-socket-io';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CommsService {
  private piDevicesSubject: BehaviorSubject<{ [piName: string]: any[] }> = new BehaviorSubject({});
  piDevices$ = this.piDevicesSubject.asObservable();
  previousTemperature = 0;
  previousHumidity = 0;

  constructor(private socket: Socket) {
    this.connectAndSubscribe();
    this.loadSetupFromLocalStorage();
    this.loadValuesFromLocalStorage();
  }

  private connectAndSubscribe() {
    this.socket.connect();
    this.subscribeToTopic('angular_setup');
    this.subscribeToTopic('values');
  }

  private subscribeToTopic(topic: string) {
    this.socket.on(topic, (message: any) => {
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
    const devices = message.devices;

    this.piDevicesSubject.next({ ...this.piDevicesSubject.value, [piName]: devices });
    this.saveSetupToLocalStorage();
  }

  private updateDeviceValues(message: any) {
    const piName = message.runs_on;
    const measurement = message.measurement;
    const value = message.value;
    const name = message.code;
    const simulated = message.simulated;

    let map = this.piDevicesSubject.value;
    let lists = map[piName];

    if (!lists) {
        console.error(`No devices found for PI: ${piName}`);
        return;
    }

    let devices: any[] = [];
    lists.forEach(element => {
      if (element.name === name) {
        if (element.name.includes('DHT')) {
          if (measurement === 'Humidity') {
            devices.push({
              "name": name,
              "humidity": value,
              "temperature": this.previousTemperature,
              "simulated": simulated,
            });
            this.previousHumidity = value;
          } else {
            devices.push({
              "name": name,
              "humidity": this.previousHumidity,
              "temperature": value,
              "simulated": simulated,
            });
            this.previousTemperature = value;
          }
        } else {
          devices.push({
            "name": name,
            [measurement]: value,
            "simulated": simulated,
          });
        }
      } else {
        devices.push(element);
      }
    });

    this.piDevicesSubject.next({ ...this.piDevicesSubject.value, [piName]: devices });
    this.saveValuesToLocalStorage();
  }

  saveSetupToLocalStorage() {
    const setupData = this.piDevicesSubject.value;
    localStorage.setItem('setupData', JSON.stringify(setupData));
  }

  loadSetupFromLocalStorage() {
    const setupData = localStorage.getItem('setupData');
    if (setupData) {
      const parsedData = JSON.parse(setupData);
      this.piDevicesSubject.next(parsedData);
    }
  }

  saveValuesToLocalStorage() {
    const valuesData = this.piDevicesSubject.value;
    localStorage.setItem('valuesData', JSON.stringify(valuesData));
  }

  loadValuesFromLocalStorage() {
    const valuesData = localStorage.getItem('valuesData');
    if (valuesData) {
      const parsedData = JSON.parse(valuesData);
      this.piDevicesSubject.next(parsedData);
    }
  }

  sendRGBValues(rgbValues: boolean[]): void {
    this.socket.emit('set_rgb', { rgb: rgbValues });
  }
}
