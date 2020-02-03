import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import pins
from esphome.components import display
from esphome.const import CONF_CLK_PIN, CONF_DIO_PIN, CONF_ID, CONF_LAMBDA, CONF_INTENSITY

tm1637_ns = cg.esphome_ns.namespace('tm1637')
TM1637Display = tm1637_ns.class_('TM1637Display', cg.PollingComponent)
TM1637DisplayRef = TM1637Display.operator('ref')

CONFIG_SCHEMA = display.BASIC_DISPLAY_SCHEMA.extend({
    cv.GenerateID(): cv.declare_id(TM1637Display),

    cv.Optional(CONF_INTENSITY, default=7): cv.All(cv.uint8_t, cv.Range(min=0, max=7)),
    cv.Required(CONF_CLK_PIN): pins.internal_gpio_output_pin_schema,
    cv.Required(CONF_DIO_PIN): pins.internal_gpio_output_pin_schema,
}).extend(cv.polling_component_schema('1s'))


def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    yield cg.register_component(var, config)
    yield display.register_display(var, config)

    clk = yield cg.gpio_pin_expression(config[CONF_CLK_PIN])
    cg.add(var.set_clk_pin(clk))
    dio = yield cg.gpio_pin_expression(config[CONF_DIO_PIN])
    cg.add(var.set_dio_pin(dio))

    cg.add(var.set_intensity(config[CONF_INTENSITY]))

    if CONF_LAMBDA in config:
        lambda_ = yield cg.process_lambda(config[CONF_LAMBDA], [(TM1637DisplayRef, 'it')],
                                          return_type=cg.void)
        cg.add(var.set_writer(lambda_))
