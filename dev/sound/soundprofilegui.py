import PySimpleGUI as sg
from audiofilegui import AudioFileGui
from soundprofile import SoundProfile
from toolbox import *

from pfxbrick import *

sp = SoundProfile()

idle_dict = [
    {
        "title": "Notch 1 loop",
        "fileid": 0xE0,
        "looped": True,
    },
    {
        "title": "Notch 2 loop",
        "fileid": 0xE1,
        "looped": True,
    },
    {
        "title": "Notch 3 loop",
        "fileid": 0xE2,
        "looped": True,
    },
    {
        "title": "Notch 4 loop",
        "fileid": 0xE3,
        "looped": True,
    },
    {
        "title": "Notch 5 loop",
        "fileid": 0xE4,
        "looped": True,
    },
    {
        "title": "Notch 6 loop",
        "fileid": 0xE5,
        "looped": True,
    },
    {
        "title": "Notch 7 loop",
        "fileid": 0xE6,
        "looped": True,
    },
    {
        "title": "Notch 8 loop",
        "fileid": 0xE7,
        "looped": True,
    },
]
accel_dict = [
    {
        "title": "Accel 1-2",
        "fileid": 0xE8,
        "looped": False,
    },
    {
        "title": "Accel 2-3",
        "fileid": 0xE9,
        "looped": False,
    },
    {
        "title": "Accel 3-4",
        "fileid": 0xEA,
        "looped": False,
    },
    {
        "title": "Accel 4-5",
        "fileid": 0xEB,
        "looped": False,
    },
    {
        "title": "Accel 5-6",
        "fileid": 0xEC,
        "looped": False,
    },
    {
        "title": "Accel 6-7",
        "fileid": 0xED,
        "looped": False,
    },
    {
        "title": "Accel 7-8",
        "fileid": 0xEE,
        "looped": False,
    },
]
decel_dict = [
    {
        "title": "Decel 2-1",
        "fileid": 0xF0,
        "looped": False,
    },
    {
        "title": "Decel 3-2",
        "fileid": 0xF1,
        "looped": False,
    },
    {
        "title": "Decel 4-3",
        "fileid": 0xF2,
        "looped": False,
    },
    {
        "title": "Decel 5-4",
        "fileid": 0xF3,
        "looped": False,
    },
    {
        "title": "Decel 6-5",
        "fileid": 0xF4,
        "looped": False,
    },
    {
        "title": "Decel 7-6",
        "fileid": 0xF5,
        "looped": False,
    },
    {
        "title": "Decel 8-7",
        "fileid": 0xF6,
        "looped": False,
    },
]

trig1_dict = [
    {
        "title": "Startup",
        "fileid": 0xEF,
        "looped": False,
    },
    {
        "title": "Change Dir",
        "fileid": 0xFA,
        "looped": False,
    },
    {
        "title": "Shutdown",
        "fileid": 0xF7,
        "looped": False,
    },
]
trig2_dict = [
    {
        "title": "Rapid Accel",
        "fileid": 0xFC,
        "looped": False,
    },
    {
        "title": "Rapid Decel",
        "fileid": 0xFD,
        "looped": False,
    },
    {
        "title": "Set Off",
        "fileid": 0xFB,
        "looped": False,
    },
    {
        "title": "Brake to Stop",
        "fileid": 0xFE,
        "looped": False,
    },
]
gated1_dict = [
    {
        "title": "Gated 1 Loop 1",
        "fileid": 0xD0,
        "looped": False,
    },
    {
        "title": "Gated 2 Loop 1",
        "fileid": 0xD4,
        "looped": False,
    },
    {
        "title": "Gated 3 Loop 1",
        "fileid": 0xD8,
        "looped": False,
    },
    {
        "title": "Gated 4 Loop 1",
        "fileid": 0xDC,
        "looped": False,
    },
]
gated2_dict = [
    {
        "title": "Gated 1 Loop 2",
        "fileid": 0xD1,
        "looped": False,
    },
    {
        "title": "Gated 2 Loop 2",
        "fileid": 0xD5,
        "looped": False,
    },
    {
        "title": "Gated 3 Loop 2",
        "fileid": 0xD9,
        "looped": False,
    },
    {
        "title": "Gated 4 Loop 2",
        "fileid": 0xDD,
        "looped": False,
    },
]
gated3_dict = [
    {
        "title": "Gated 1 Loop 3",
        "fileid": 0xD2,
        "looped": False,
    },
    {
        "title": "Gated 2 Loop 3",
        "fileid": 0xD6,
        "looped": False,
    },
    {
        "title": "Gated 3 Loop 3",
        "fileid": 0xDA,
        "looped": False,
    },
    {
        "title": "Gated 4 Loop 3",
        "fileid": 0xDE,
        "looped": False,
    },
]
gated4_dict = [
    {
        "title": "Gated 1 Loop 4",
        "fileid": 0xD3,
        "looped": False,
    },
    {
        "title": "Gated 2 Loop 4",
        "fileid": 0xD7,
        "looped": False,
    },
    {
        "title": "Gated 3 Loop 4",
        "fileid": 0xDB,
        "looped": False,
    },
    {
        "title": "Gated 4 Loop 4",
        "fileid": 0xDF,
        "looped": False,
    },
]

sliders = [
    sg.Frame(
        "Accel Thr",
        [
            [
                sg.Slider(
                    range=(0, 120),
                    orientation="v",
                    resolution=1,
                    tick_interval=20,
                    key="-accelthr-",
                    size=(10, 20),
                    enable_events=True,
                )
            ]
        ],
    ),
    sg.Frame(
        "Decel Thr",
        [
            [
                sg.Slider(
                    range=(0, 120),
                    orientation="v",
                    resolution=1,
                    tick_interval=20,
                    key="-decelthr-",
                    size=(10, 20),
                    enable_events=True,
                )
            ]
        ],
    ),
    sg.Frame(
        "Brake Speed",
        [
            [
                sg.Slider(
                    range=(0, 250),
                    orientation="v",
                    resolution=1,
                    tick_interval=50,
                    key="-brakespeed-",
                    size=(10, 20),
                    enable_events=True,
                )
            ]
        ],
    ),
    sg.Frame(
        "Brake Thr",
        [
            [
                sg.Slider(
                    range=(0, 120),
                    orientation="v",
                    resolution=1,
                    tick_interval=20,
                    key="-brakethr-",
                    size=(10, 20),
                    enable_events=True,
                )
            ]
        ],
    ),
]
notch_cfg = [
    sg.Frame(
        "Notches",
        [
            [
                sg.Spin(
                    values=list(range(1, 9)),
                    key="-notchcount-",
                    size=(5, 1),
                    enable_events=True,
                )
            ]
        ],
    ),
    sg.Frame(
        "Notch Bounds",
        [
            [
                sg.Input(
                    key="-bound%d-" % (x),
                    size=(6, 1),
                    use_readonly_for_disable=True,
                    disabled_readonly_background_color="#909090",
                )
                for x in range(7)
            ]
        ],
    ),
]

af_decel = [AudioFileGui(**k) for k in decel_dict]
af_idle = [AudioFileGui(**k) for k in idle_dict]
af_accel = [AudioFileGui(**k) for k in accel_dict]
af_trig1 = [AudioFileGui(**k) for k in trig1_dict]
af_trig2 = [AudioFileGui(**k) for k in trig2_dict]
af_gated1 = [AudioFileGui(**k) for k in gated1_dict]
af_gated2 = [AudioFileGui(**k) for k in gated2_dict]
af_gated3 = [AudioFileGui(**k) for k in gated3_dict]
af_gated4 = [AudioFileGui(**k) for k in gated4_dict]

af_all = []
af_all.extend(af_decel)
af_all.extend(af_idle)
af_all.extend(af_accel)
af_all.extend(af_trig1)
af_all.extend(af_trig2)
af_all.extend(af_gated1)
af_all.extend(af_gated2)
af_all.extend(af_gated3)
af_all.extend(af_gated4)

af_bell = AudioFileGui(title="Bell", fileid=0xF8, looped=True)
af_short = AudioFileGui(title="Short Whistle", fileid=0xF9, looped=False)
af_long = AudioFileGui(title="Long Whistle", fileid=0xCF, looped=False)
af_all.append(af_bell)
af_all.append(af_short)
af_all.append(af_long)

layout = [
    [
        notch_cfg,
        sg.Column([af_bell.get_layout()]),
        sg.Column([af_short.get_layout()]),
        sg.Column([af_long.get_layout()]),
    ],
    [
        *(sg.Column([af.get_layout()]) for af in af_trig1),
        sg.Frame(
            "Gated Gain",
            [
                [
                    sg.Slider(
                        range=(0, 100),
                        orientation="h",
                        resolution=1,
                        tick_interval=20,
                        key="-gatedgain-",
                        size=(20, 10),
                        enable_events=True,
                    )
                ]
            ],
        ),
        sg.Frame(
            "Acceleration",
            [
                [
                    sg.Slider(
                        range=(0, 15),
                        orientation="h",
                        resolution=1,
                        tick_interval=5,
                        key="-accel-",
                        size=(20, 10),
                        enable_events=True,
                    )
                ]
            ],
        ),
        sg.Frame(
            "Deceleration",
            [
                [
                    sg.Slider(
                        range=(0, 15),
                        orientation="h",
                        resolution=1,
                        tick_interval=5,
                        key="-decel-",
                        size=(20, 10),
                        enable_events=True,
                    )
                ]
            ],
        ),
    ],
    [
        sg.Column([af.get_layout() for af in af_decel]),
        sg.Column([af.get_layout() for af in af_idle]),
        sg.Column([af.get_layout() for af in af_accel]),
        sg.Column(
            [
                *(af.get_layout() for af in af_gated1),
                AudioFileGui(**trig2_dict[0]).get_layout(),
                [sliders[0]],
            ]
        ),
        sg.Column(
            [
                *(af.get_layout() for af in af_gated2),
                AudioFileGui(**trig2_dict[1]).get_layout(),
                [sliders[1]],
            ]
        ),
        sg.Column(
            [
                *(af.get_layout() for af in af_gated3),
                AudioFileGui(**trig2_dict[2]).get_layout(),
                [sliders[2]],
            ]
        ),
        sg.Column(
            [
                *(af.get_layout() for af in af_gated4),
                AudioFileGui(**trig2_dict[3]).get_layout(),
                [sliders[3]],
            ]
        ),
    ],
    [
        sg.Button("Read Brick", key="-readbrick-"),
        sg.Input(visible=False, enable_events=True, key="-inputfile-"),
        sg.FileBrowse("Import YAML"),
        sg.Input(visible=False, enable_events=True, key="-exportscript-"),
        sg.FileBrowse("Export Script"),
        sg.Button("Copy to Brick", key="-copytobrick-"),
        sg.Button("Export Profile", key="-exportprofile-"),
    ],
]


def update_audio_file(audiofile):
    for f in af_all:
        if audiofile is not None:
            if f.fileid == audiofile.fileid:
                f.set_audiofile(audiofile)
                return
    f.clear()


def update_gui(window, event, values):
    for f in af_all:
        # f.process_event(event)
        f.update()

    for x in range(7):
        key = "-bound%d-" % (x)
        disabled = False if x < sp.notch_count - 1 else True
        window[key].update(disabled=disabled)


def update_with_profile(window):
    window["-notchcount-"].update("%d" % (sp.notch_count))
    for x in range(sp.notch_count - 1):
        key = "-bound%d-" % (x)
        window[key].update("%d" % (sp.notch_bounds[x]))
    for x in range(7):
        key = "-bound%d-" % (x)
        disabled = False if x < sp.notch_count - 1 else True
        window[key].update(disabled=disabled)
    window["-accel-"].update("%d" % (sp.acceleration))
    window["-decel-"].update("%d" % (sp.deceleration))
    if sp.rapid_accel_thr is not None:
        window["-accelthr-"].update("%d" % (sp.rapid_accel_thr))
    if sp.rapid_decel_thr is not None:
        window["-decelthr-"].update("%d" % (sp.rapid_decel_thr))
    if sp.brake_decel_thr is not None:
        window["-brakethr-"].update("%d" % (sp.brake_decel_thr))
    if sp.brake_speed_thr is not None:
        window["-brakespeed-"].update("%d" % (sp.brake_speed_thr))
    if sp.gated_gain is not None:
        window["-gatedgain-"].update("%d" % (sp.gated_gain))
    update_audio_file(sp.startup)
    update_audio_file(sp.shutdown)
    update_audio_file(sp.change_dir_sound)
    update_audio_file(sp.rapid_accel_loop)
    update_audio_file(sp.rapid_decel_loop)
    update_audio_file(sp.brake_stop_sound)
    update_audio_file(sp.set_off_sound)
    update_audio_file(sp.bell)
    update_audio_file(sp.short_whistle)
    update_audio_file(sp.long_whistle)
    if sp.idle_loops is not None:
        for el in sp.idle_loops.loops:
            update_audio_file(el)
    if sp.accel_loops is not None:
        for el in sp.accel_loops.loops:
            update_audio_file(el)
    if sp.decel_loops is not None:
        for el in sp.decel_loops.loops:
            update_audio_file(el)
    if sp.gated_loops is not None:
        for el in sp.gated_loops.loops:
            update_audio_file(el)


def main():
    # Create the window
    window = sg.Window(
        "PFx Brick Sound Profile", layout, element_padding=(2, 2), font="Any 12"
    )
    for f in af_all:
        f.set_graph_el(window)
        f.parent = window
    window.finalize()

    # Display and interact with the Window using an Event Loop
    while True:
        event, values = window.read()
        # See if user wants to quit or window was closed
        if event == sg.WINDOW_CLOSED or event == "Quit":
            break
        elif event == "-inputfile-":
            fs = FileOps()
            if not fs.verify_dir_not_file(values["-inputfile-"]):
                proj = Params(yml=values["-inputfile-"])
                sp.clear()
                sp.set_with_dict(proj.__dict__)
                update_with_profile(window)
        elif event == "-notchcount-":
            sp.notch_count = values["-notchcount-"]
            for f in af_all:
                f.set_notch_count(sp.notch_count)
                f.update()
        elif event == "-exportscript-":
            sp.export_script(values["-exportscript-"])
        elif event == "-copytobrick-":
            for af in af_all:
                af.show_progress = False
                af.update()
            window.refresh()
            brick = PFxBrick()
            r = brick.open()
            if r:
                halt_action = PFxAction()
                halt_action.command = EVT_COMMAND_ALL_OFF
                brick.test_action(halt_action)
                brick.refresh_file_dir()
                for af in af_all:
                    if af.is_valid():
                        af.copy_to_brick(brick)
                    window.refresh()
                for af in sp.other_sounds:
                    print(af["audiofile"])
                    af["audiofile"].copy_to_brick(brick)
                sp.export_script("startup.pfx", as_bytes=True, to_brick=brick)
                brick.close()

        elif event == "-exportprofile-":
            brick = PFxBrick()
            r = brick.open()
            if r:
                brick.get_config()
                sp.export_pfx_profile("test.pfxconfig", brick, af_all)
            brick.close()
        elif event == "-accelthr-":
            sp.rapid_accel_thr = int(values["-accelthr-"])
        elif event == "-decelthr-":
            sp.rapid_decel_thr = int(values["-decelthr-"])
        elif event == "-brakethr-":
            sp.brake_decel_thr = int(values["-brakethr-"])
        elif event == "-brakespeed-":
            sp.brake_speed_thr = int(values["-brakespeed-"])
        elif event == "-gatedgain-":
            sp.gated_gain = int(values["-gatedgain-"])
        else:
            for f in af_all:
                f.process_event(event, values, sp)

        update_gui(window, event, values)

    # Finish up by removing from the screen
    window.close()


if __name__ == "__main__":
    main()
