import unittest

from xknx import XKNX,Light,Address,Telegram,TelegramType,DPT_Binary,DPT_Array

class TestLight(unittest.TestCase):

    #
    # REQUEST STATE
    #
    def test_request_state(self):

        xknx = XKNX()
        light = Light(xknx, "TestLight", {'group_address_switch':'1/2/3', 'group_address_dimm':'1/2/4','group_address_dimm_feedback':'1/2/5'})
        light.request_state()

        self.assertEqual( xknx.telegrams.qsize(), 2 )

        telegram1 = xknx.telegrams.get()
        self.assertEqual( telegram1, Telegram(Address('1/2/3'), TelegramType.GROUP_READ) )

        telegram2 = xknx.telegrams.get()
        self.assertEqual( telegram2, Telegram(Address('1/2/5'), TelegramType.GROUP_READ) )


    #
    # TEST SET ON
    #
    def test_set_on(self):
        xknx = XKNX()
        light = Light(xknx, "TestLight", {'group_address_switch':'1/2/3', 'group_address_dimm':'1/2/4','group_address_dimm_feedback':'1/2/5'})
        light.set_on()
        self.assertEqual( xknx.telegrams.qsize(), 1 )
        telegram = xknx.telegrams.get()
        self.assertEqual( telegram, Telegram(Address('1/2/3'),  payload=DPT_Binary(1) ) )

    #
    # TEST SET OFF
    #
    def test_set_off(self):
        xknx = XKNX()
        light = Light(xknx, "TestLight", {'group_address_switch':'1/2/3', 'group_address_dimm':'1/2/4','group_address_dimm_feedback':'1/2/5'})
        light.set_off()
        self.assertEqual( xknx.telegrams.qsize(), 1 )
        telegram = xknx.telegrams.get()
        self.assertEqual( telegram, Telegram(Address('1/2/3'),  payload=DPT_Binary(0) ) )

    #
    # TEST SET BRIGHTNESS
    #
    def test_set_off(self):
        xknx = XKNX()
        light = Light(xknx, "TestLight", {'group_address_switch':'1/2/3', 'group_address_dimm':'1/2/4','group_address_dimm_feedback':'1/2/5'})
        light.set_brightness(23)
        self.assertEqual( xknx.telegrams.qsize(), 1 )
        telegram = xknx.telegrams.get()
        self.assertEqual( telegram, Telegram(Address('1/2/5'), payload=DPT_Array(23) ) )


    #
    # TEST PROCESS
    #
    def test_process_switch(self):
        xknx = XKNX()
        light = Light(xknx, "TestLight", {'group_address_switch':'1/2/3', 'group_address_dimm':'1/2/4','group_address_dimm_feedback':'1/2/5'})
        self.assertEqual( light.state, False )

        telegram = Telegram(Address('1/2/3'), payload=DPT_Binary(1))
        light.process( telegram )
        self.assertEqual( light.state, True )

        telegram = Telegram(Address('1/2/3'), payload=DPT_Binary(0))
        light.process( telegram )
        self.assertEqual( light.state, False )


    def test_process_dimm(self):
        xknx = XKNX()
        light = Light(xknx, "TestLight", {'group_address_switch':'1/2/3', 'group_address_dimm':'1/2/4','group_address_dimm_feedback':'1/2/5'})
        self.assertEqual( light.brightness, 0 )

        telegram = Telegram(Address('1/2/5'), payload = DPT_Array(23))
        light.process( telegram )
        self.assertEqual( light.brightness, 23 )




suite = unittest.TestLoader().loadTestsFromTestCase(TestLight)
unittest.TextTestRunner(verbosity=2).run(suite)