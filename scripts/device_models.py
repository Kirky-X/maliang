#!/usr/bin/env python3
"""设备尺寸配置 —— preview 子命令的单一数据源。

用法:
    from device_models import get_device, list_devices, Device

    device = get_device("iphone-15-pro-max")
    print(device.width, device.height)  # 430 932

    for d in list_devices():
        print(d.name, d.width, d.height)

依赖: Python 3 标准库(无第三方依赖)。
契约: 设备尺寸为硬编码常量(确定性数据),禁止由 LLM 推断或运行时计算。
新增设备时只需在 DEVICES 列表中添加条目。
"""
from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class Device:
    """设备尺寸配置。

    Attributes:
        id: 设备唯一标识(kebab-case,用于查询)
        name: 设备显示名称
        platform: 平台(ios / android)
        device_type: 设备类型(phone / tablet)
        width: 屏幕宽度(px,CSS 像素)
        height: 屏幕高度(px,CSS 像素)
        has_notch: 是否有刘海(手机通常有,平板通常无)
        corner_radius: 设备外壳圆角(px)
        border_width: 设备外壳边框宽度(px)
    """
    id: str
    name: str
    platform: str
    device_type: str
    width: int
    height: int
    has_notch: bool
    corner_radius: int
    border_width: int


# ---------------------------------------------------------------------------
# 设备尺寸常量(硬编码,确定性数据)
# 数据来源:各设备官方规格页面(2026-07-01 校验)
# ---------------------------------------------------------------------------

IPHONE_15_PRO_MAX = Device(
    id="iphone-15-pro-max",
    name="iPhone 15 Pro Max",
    platform="ios",
    device_type="phone",
    width=430,
    height=932,
    has_notch=True,
    corner_radius=55,
    border_width=12,
)

IPHONE_15 = Device(
    id="iphone-15",
    name="iPhone 15",
    platform="ios",
    device_type="phone",
    width=393,
    height=852,
    has_notch=True,
    corner_radius=48,
    border_width=11,
)

IPHONE_SE_3RD = Device(
    id="iphone-se-3rd",
    name="iPhone SE 3rd",
    platform="ios",
    device_type="phone",
    width=375,
    height=667,
    has_notch=False,
    corner_radius=40,
    border_width=10,
)

IPAD_PRO_12_9 = Device(
    id="ipad-pro-12-9",
    name='iPad Pro 12.9"',
    platform="ios",
    device_type="tablet",
    width=1024,
    height=1366,
    has_notch=False,
    corner_radius=28,
    border_width=14,
)

IPAD_AIR = Device(
    id="ipad-air",
    name="iPad Air",
    platform="ios",
    device_type="tablet",
    width=820,
    height=1180,
    has_notch=False,
    corner_radius=24,
    border_width=12,
)

SAMSUNG_GALAXY_TAB_S8 = Device(
    id="samsung-galaxy-tab-s8",
    name="Samsung Galaxy Tab S8",
    platform="android",
    device_type="tablet",
    width=1600,
    height=2560,
    has_notch=False,
    corner_radius=20,
    border_width=10,
)


# ---------------------------------------------------------------------------
# 设备注册表(新增设备时在此列表追加)
# ---------------------------------------------------------------------------

DEVICES: List[Device] = [
    IPHONE_15_PRO_MAX,
    IPHONE_15,
    IPHONE_SE_3RD,
    IPAD_PRO_12_9,
    IPAD_AIR,
    SAMSUNG_GALAXY_TAB_S8,
]


# ---------------------------------------------------------------------------
# 查询函数
# ---------------------------------------------------------------------------

def list_devices() -> List[Device]:
    """返回全部已注册设备列表。"""
    return list(DEVICES)


def list_devices_by_type(device_type: str) -> List[Device]:
    """按设备类型过滤(phone / tablet)。"""
    return [d for d in DEVICES if d.device_type == device_type]


def list_devices_by_platform(platform: str) -> List[Device]:
    """按平台过滤(ios / android)。"""
    return [d for d in DEVICES if d.platform == platform]


def get_device(device_id: str) -> Optional[Device]:
    """按设备 ID 查询。未找到返回 None。"""
    for d in DEVICES:
        if d.id == device_id:
            return d
    return None


def get_device_or_die(device_id: str) -> Device:
    """按设备 ID 查询。未找到抛出 KeyError。"""
    device = get_device(device_id)
    if device is None:
        raise KeyError("未知设备 ID: {},可用 ID: {}".format(
            device_id, ", ".join(d.id for d in DEVICES)
        ))
    return device


def device_to_css(device: Device) -> str:
    """将设备尺寸转为 CSS 变量字符串(用于 HTML 模板注入)。"""
    return (
        "    --device-width: {w}px;\n"
        "    --device-height: {h}px;\n"
        "    --device-corner-radius: {cr}px;\n"
        "    --device-border-width: {bw}px;\n"
        "    --device-has-notch: {notch};"
    ).format(
        w=device.width,
        h=device.height,
        cr=device.corner_radius,
        bw=device.border_width,
        notch="1" if device.has_notch else "0",
    )


# ---------------------------------------------------------------------------
# CLI 入口(python3 scripts/device_models.py [list|<device-id>])
# ---------------------------------------------------------------------------

def main(argv):
    if len(argv) <= 1 or argv[1] == "list":
        print("{:<28} {:<8} {:<8} {:<10} {:<10} {}".format(
            "ID", "平台", "类型", "宽度", "高度", "名称"
        ))
        for d in DEVICES:
            print("{:<28} {:<8} {:<8} {:<10} {:<10} {}".format(
                d.id, d.platform, d.device_type, d.width, d.height, d.name
            ))
        return 0
    device_id = argv[1]
    try:
        device = get_device_or_die(device_id)
    except KeyError as e:
        print("[error] {}".format(e), flush=True)
        return 1
    print("ID: {}".format(device.id))
    print("名称: {}".format(device.name))
    print("平台: {}".format(device.platform))
    print("类型: {}".format(device.device_type))
    print("尺寸: {}x{}".format(device.width, device.height))
    print("刘海: {}".format("有" if device.has_notch else "无"))
    print("圆角: {}px".format(device.corner_radius))
    print("边框: {}px".format(device.border_width))
    print()
    print("CSS 变量:")
    print(device_to_css(device))
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv))
