import { Component } from '@angular/core';
import { CommsService } from '../comms.service';

@Component({
  selector: 'app-manage',
  templateUrl: './manage.component.html',
  styleUrls: ['./manage.component.css']
})
export class ManageComponent {

  constructor(private commsService: CommsService) {}

  selectedColor: string = ''; // Initialize with empty string for "Select a color"

  colorMappings: { [key: string]: boolean[] } = {
    'white': [true, true, true],
    'red': [true, false, false],
    'green': [false, true, false],
    'blue': [false, false, true],
    'yellow': [true, true, false],
    'purple': [true, false, true],
    'lightBlue': [false, true, true],
    'off': [false, false, false],
  };

  applyColor(): void {
    if (this.selectedColor) { // Ensure a color is selected
      const rgbValues: boolean[] = this.colorMappings[this.selectedColor];
      console.log(`Applying RGB values: ${rgbValues}`);
      this.commsService.sendRGBValues(rgbValues);
    } else {
      alert('Please select a color before applying.');
      // Optionally, notify the user to select a color
    }
  }
}
