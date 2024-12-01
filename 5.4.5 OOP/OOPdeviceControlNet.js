function Net(devices){                             //сеть как отдельный класс

    this.devices = devices                                 //массив девайсов

    Net.prototype.getDevicesConsumption = function(){              //функция печатает нагруженость сети в текущий момент
        let powerfull = 0
        for (let obj in this.devices){
                powerfull += this.devices[obj].powerInstant;
        }
        console.log(`${powerfull}w Current network load`)
    }
    
    Net.prototype.printListDevicesOnNet = function(){               //печатает в консоль все устройства включеные в сеть
        for (let obj in this.devices){
            if (this.devices[obj].getOnOrOff()){
                console.log(`${this.devices[obj].name} powerOnIns ${this.devices[obj].powerInstant}w`)
            } else {
                console.log(`${this.devices[obj].name} powerOffIns ${this.devices[obj].powerInstant}w`)
            }
        }
    }

}

function Device(name){                      //родительский класс устройств где name имя устройства
                             
    this.name = name
    this.OnOrOff = false
    this.powerInstant = 0

    Device.prototype.getOnOrOff = function(){   //родительский метод определения включено или выключенно устроство 
        return this.OnOrOff
    }     
    
    Device.prototype.deviceOn = function(){                         //метод включения устройства
        this.OnOrOff = true
        this.powerInstant = this.getPower();
        console.log(`${this.name} powerOn ${this.powerInstant}w`)
    }

    Device.prototype.deviceOff = function(){                        //метод выключения устройства
        this.OnOrOff = false
        this.powerInstant = this.getPower();
        console.log(`${this.name} powerOff ${this.powerInstant}w`)
    }

    Device.prototype.getPower = function(){                         //родительский метод определения текущей потребляемой электроэнергии
        if (this.getOnOrOff){
            this.powerInstant = this.getPower();
        } else{
            this.powerInstant = 0
        }
    }
}

function DeviceComputer(name, powerMin, powerMax){
    this.name = name
    this.powerMin = powerMin
    this.powerMax = powerMax

    DeviceComputer.prototype.getPower = function(){     
        if  (this.getOnOrOff()){                                                                  //у каждого устройства потребляемая мощность вычесляется по разному 
            return ((Math.random() * (this.powerMax - this.powerMin + 1)) + this.powerMin)    //и будет записываться в момент его запуска у объекта и перезаписываться
        } else {                                                                                  //каждый раз после включения или отключения
            return this.powerMin/100                                                              //даже у отключеных устройств есть потребление, например отключеные блоки питания тоже кушают электроэнергию
        }                                                                                         //для подзаряда конденцаторов
    }                                                               
}

function DeviceBulb(name, power){
    this.name = name
    this.power = power

    DeviceBulb.prototype.getPower = function(){
        if (this.getOnOrOff()){
            return this.power
        } else{
            return 0
        }
    }
}

DeviceComputer.prototype = new Device();
DeviceBulb.prototype = new Device();
const com1 = new DeviceComputer('IBN5100', 400, 1000);
const com2 = new DeviceComputer('Asus AN500', 300, 450);
const bulb1 = new DeviceBulb('incandescent lamp', 110);
const bulb2 = new DeviceBulb('LED lamp', 15);
const devices = [com1, com2, bulb1, bulb2];
const network = new Net(devices);
com1.deviceOn();
com2.deviceOn();
bulb1.deviceOn();
bulb2.deviceOn();
network.getDevicesConsumption();
com2.deviceOff();
network.getDevicesConsumption();
com2.deviceOn();
network.getDevicesConsumption();
bulb2.deviceOff();
network.getDevicesConsumption();
bulb1.deviceOff();
network.getDevicesConsumption();
network.printListDevicesOnNet();