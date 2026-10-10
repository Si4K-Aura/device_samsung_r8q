$(call inherit-product, $(SRC_TARGET_DIR)/product/base.mk)
$(call inherit-product, vendor/twrp/config/common.mk)

# Dynamic partitions (the device launched with Android 10 = API 29)
PRODUCT_USE_DYNAMIC_PARTITIONS := true
PRODUCT_SHIPPING_API_LEVEL := 29

PRODUCT_DEVICE := r8q
PRODUCT_NAME := twrp_r8q
PRODUCT_BRAND := samsung
PRODUCT_MODEL := Galaxy S20 FE 5G
PRODUCT_MANUFACTURER := samsung
PRODUCT_RELEASE_NAME := Galaxy S20 FE 5G
