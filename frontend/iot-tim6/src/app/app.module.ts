import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NavbarComponent } from './navbar/navbar.component';
import { DevicesComponent } from './devices/devices.component';
import { AlarmsComponent } from './alarms/alarms.component';
import { TimersComponent } from './timers/timers.component';
import { ManageComponent } from './manage/manage.component';
import { FormsModule } from '@angular/forms';

import { SocketIoModule, SocketIoConfig } from 'ngx-socket-io';
import { HttpClientModule } from '@angular/common/http';

const config: SocketIoConfig = { url: 'http://localhost:5000/angular', options: {} };

@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    DevicesComponent,
    AlarmsComponent,
    TimersComponent,
    ManageComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    SocketIoModule.forRoot(config),
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
