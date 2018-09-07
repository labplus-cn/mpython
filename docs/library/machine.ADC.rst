.. currentmodule:: machine
.. _machine.ADC:

类 ADC -- 模数转换
=========================================

示例::

   import machine

   adc = machine.ADC()             # create an ADC object
   apin = adc.channel(pin='GP3')   # create an analog pin on GP3
   val = apin()                    # read an analog value

构建函数
------------

.. class:: ADC(id=0, \*, bits=12)

创建与设定引脚关联的ADC对象。这样您就可以读取该引脚上的模拟值。

有关更多信息，请查看 `ESP32引脚功能表. <../../../images/esp32_pinout.png>`_ 

   .. warning:: 

      ADC pin input range is 0-1.4V (being 1.8V the absolute maximum that it 
      can withstand). When GP2, GP3, GP4 or GP5 are remapped to the 
      ADC block, 1.8 V is the maximum. If these pins are used in digital mode, 
      then the maximum allowed input is 3.6V.

Methods
-------

.. method:: ADC.channel(id, \*, pin)

   Create an analog pin. If only channel ID is given, the correct pin will
   be selected. Alternatively, only the pin can be passed and the correct
   channel will be selected. Examples::

      # all of these are equivalent and enable ADC channel 1 on GP3
      apin = adc.channel(1)
      apin = adc.channel(pin='GP3')
      apin = adc.channel(id=1, pin='GP3')

.. method:: ADC.init()

   Enable the ADC block.

.. method:: ADC.deinit()

   Disable the ADC block.

class ADCChannel --- read analog values from internal or external sources
=========================================================================

ADC channels can be connected to internal points of the MCU or to GPIO pins.
ADC channels are created using the ADC.channel method.

.. method:: adcchannel()

   Fast method to read the channel value.

.. method:: adcchannel.value()

   Read the channel value.

.. method:: adcchannel.init()

   Re-init (and effectively enable) the ADC channel.

.. method:: adcchannel.deinit()

   Disable the ADC channel.
