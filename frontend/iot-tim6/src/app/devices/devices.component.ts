// devices.component.ts

import { Component } from '@angular/core';

@Component({
  selector: 'app-devices',
  templateUrl: './devices.component.html',
  styleUrls: ['./devices.component.css']
})
export class DevicesComponent {
  selectedPi: string = 'PI1';
  devicesList: any[] = [];

  piDevicesMap: any = {
    'PI1': [
      { name: 'Device 1', info: ['Info 1 - SkrapapaSkrapapaSkrapapaSkrapapaSkrapapa', 'Info 2 - Skrapapa', 'Info 3 - Skrapapa'] },
      { name: 'Device 1', info: ['Info 1'] },
      { name: 'Device 1', info: ['Info 1 - Skrapapa', 'Info 2 - Skrapapa', 'Info 3 - Skrapapa'] },
      { name: 'Device 1', info: ['Info 1 - Skrapapa', 'Info 2 - Skrapapa', 'Info 3 - Skrapapa'] },
      { name: 'Device 1', info: ['Info 1', 'Info 2', ] },
      { name: 'Device 1', info: ['Info 1', 'Info 2', 'Info 3'] },
      { name: 'Device 1', info: ['Info 1 - Skrapapa', 'Info 2 - Skrapapa', 'Info 3 - Skrapapa'] },
      { name: 'Device 1', info: ['Info 1', ] },
      { name: 'Device 1', info: ['Info 1', 'Info 2'] },
      { name: 'Device 1', info: ['Info 1', 'Info 2', 'Info 3'] },
    ],
    'PI2': [
      // Devices for PI2
    ],
    'PI3': [
      // Devices for PI3
    ],
    // Add more Raspberry Pi entries as needed
  };

  ngOnInit() {
    this.updateDevicesList();
  }

  updateDevicesList() {
    this.devicesList = this.piDevicesMap[this.selectedPi];
  }
}
