from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import analog
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import sip



class qam_qcm(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "qam_qcm")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 48000

        ##################################################
        # Blocks
        ##################################################

        self.quadrature_carrier = blocks.phase_shift(90, False)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_f(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)


        self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.multiplexed_signal = blocks.add_vcc(1)
        self.m2 = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, 4000, 1, 0, 0)
        self.m1 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 1000, 1, 0, 0)
        self.low_pass_filter_1 = filter.fir_filter_fff(
            1,
            firdes.low_pass(
                1.5,
                samp_rate,
                3800,
                300,
                window.WIN_HAMMING,
                6.76))
        self.low_pass_filter_0 = filter.fir_filter_fff(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                800,
                300,
                window.WIN_HAMMING,
                6.76))
        self.inphase_Demodulator = blocks.multiply_vff(1)
        self.inPhase_Product_Modulator = blocks.multiply_vcc(1)
        self.blocks_throttle2_2_1_0 = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_throttle2_2_1 = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_throttle2_2_0 = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_throttle2_1_1 = blocks.throttle( gr.sizeof_float*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_throttle2_1_0 = blocks.throttle( gr.sizeof_float*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_float*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0) * samp_rate) if "auto" == "time" else int(0), 1) )
        self.blocks_complex_to_real_0_3 = blocks.complex_to_real(1)
        self.blocks_complex_to_real_0_2_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_real_0_2 = blocks.complex_to_real(1)
        self.Recovered_Signal_m2_1 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            'recieved_m2', #name
            1, #number of inputs
            None # parent
        )
        self.Recovered_Signal_m2_1.set_update_time(0.10)
        self.Recovered_Signal_m2_1.set_y_axis(-1, 1)

        self.Recovered_Signal_m2_1.set_y_label('Amplitude', "")

        self.Recovered_Signal_m2_1.enable_tags(True)
        self.Recovered_Signal_m2_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.Recovered_Signal_m2_1.enable_autoscale(True)
        self.Recovered_Signal_m2_1.enable_grid(True)
        self.Recovered_Signal_m2_1.enable_axis_labels(True)
        self.Recovered_Signal_m2_1.enable_control_panel(False)
        self.Recovered_Signal_m2_1.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['red', 'dark blue', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.Recovered_Signal_m2_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.Recovered_Signal_m2_1.set_line_label(i, labels[i])
            self.Recovered_Signal_m2_1.set_line_width(i, widths[i])
            self.Recovered_Signal_m2_1.set_line_color(i, colors[i])
            self.Recovered_Signal_m2_1.set_line_style(i, styles[i])
            self.Recovered_Signal_m2_1.set_line_marker(i, markers[i])
            self.Recovered_Signal_m2_1.set_line_alpha(i, alphas[i])

        self._Recovered_Signal_m2_1_win = sip.wrapinstance(self.Recovered_Signal_m2_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._Recovered_Signal_m2_1_win)
        self.Recovered_Signal_m2 = qtgui.time_sink_c(
            1024, #size
            samp_rate, #samp_rate
            'M2', #name
            1, #number of inputs
            None # parent
        )
        self.Recovered_Signal_m2.set_update_time(0.10)
        self.Recovered_Signal_m2.set_y_axis(-1, 1)

        self.Recovered_Signal_m2.set_y_label('Amplitude', "")

        self.Recovered_Signal_m2.enable_tags(True)
        self.Recovered_Signal_m2.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.Recovered_Signal_m2.enable_autoscale(True)
        self.Recovered_Signal_m2.enable_grid(True)
        self.Recovered_Signal_m2.enable_axis_labels(True)
        self.Recovered_Signal_m2.enable_control_panel(False)
        self.Recovered_Signal_m2.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['red', 'dark blue', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1, 0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.Recovered_Signal_m2.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.Recovered_Signal_m2.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.Recovered_Signal_m2.set_line_label(i, labels[i])
            self.Recovered_Signal_m2.set_line_width(i, widths[i])
            self.Recovered_Signal_m2.set_line_color(i, colors[i])
            self.Recovered_Signal_m2.set_line_style(i, styles[i])
            self.Recovered_Signal_m2.set_line_marker(i, markers[i])
            self.Recovered_Signal_m2.set_line_alpha(i, alphas[i])

        self._Recovered_Signal_m2_win = sip.wrapinstance(self.Recovered_Signal_m2.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._Recovered_Signal_m2_win)
        self.Recovered_Signal_m1_1 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            'recieved_m1', #name
            1, #number of inputs
            None # parent
        )
        self.Recovered_Signal_m1_1.set_update_time(0.10)
        self.Recovered_Signal_m1_1.set_y_axis(-1, 1)

        self.Recovered_Signal_m1_1.set_y_label('Amplitude', "")

        self.Recovered_Signal_m1_1.enable_tags(True)
        self.Recovered_Signal_m1_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.Recovered_Signal_m1_1.enable_autoscale(True)
        self.Recovered_Signal_m1_1.enable_grid(True)
        self.Recovered_Signal_m1_1.enable_axis_labels(True)
        self.Recovered_Signal_m1_1.enable_control_panel(False)
        self.Recovered_Signal_m1_1.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'dark blue', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.Recovered_Signal_m1_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.Recovered_Signal_m1_1.set_line_label(i, labels[i])
            self.Recovered_Signal_m1_1.set_line_width(i, widths[i])
            self.Recovered_Signal_m1_1.set_line_color(i, colors[i])
            self.Recovered_Signal_m1_1.set_line_style(i, styles[i])
            self.Recovered_Signal_m1_1.set_line_marker(i, markers[i])
            self.Recovered_Signal_m1_1.set_line_alpha(i, alphas[i])

        self._Recovered_Signal_m1_1_win = sip.wrapinstance(self.Recovered_Signal_m1_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._Recovered_Signal_m1_1_win)
        self.Recovered_Signal_m1 = qtgui.time_sink_c(
            1024, #size
            samp_rate, #samp_rate
            'M1', #name
            1, #number of inputs
            None # parent
        )
        self.Recovered_Signal_m1.set_update_time(0.10)
        self.Recovered_Signal_m1.set_y_axis(-1, 1)

        self.Recovered_Signal_m1.set_y_label('Amplitude', "")

        self.Recovered_Signal_m1.enable_tags(True)
        self.Recovered_Signal_m1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.Recovered_Signal_m1.enable_autoscale(True)
        self.Recovered_Signal_m1.enable_grid(True)
        self.Recovered_Signal_m1.enable_axis_labels(True)
        self.Recovered_Signal_m1.enable_control_panel(False)
        self.Recovered_Signal_m1.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['dark blue', 'dark blue', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1, 0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.Recovered_Signal_m1.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.Recovered_Signal_m1.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.Recovered_Signal_m1.set_line_label(i, labels[i])
            self.Recovered_Signal_m1.set_line_width(i, widths[i])
            self.Recovered_Signal_m1.set_line_color(i, colors[i])
            self.Recovered_Signal_m1.set_line_style(i, styles[i])
            self.Recovered_Signal_m1.set_line_marker(i, markers[i])
            self.Recovered_Signal_m1.set_line_alpha(i, alphas[i])

        self._Recovered_Signal_m1_win = sip.wrapinstance(self.Recovered_Signal_m1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._Recovered_Signal_m1_win)
        self.Quadrature_Product_Modulator = blocks.multiply_vcc(1)
        self.Quadrature_Demodulator = blocks.multiply_vff(1)
        self.Multiplexed_Signal_time_Domain = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            'Multiplexed signal', #name
            1, #number of inputs
            None # parent
        )
        self.Multiplexed_Signal_time_Domain.set_update_time(0.10)
        self.Multiplexed_Signal_time_Domain.set_y_axis(-1, 1)

        self.Multiplexed_Signal_time_Domain.set_y_label('Amplitude', "")

        self.Multiplexed_Signal_time_Domain.enable_tags(True)
        self.Multiplexed_Signal_time_Domain.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.Multiplexed_Signal_time_Domain.enable_autoscale(True)
        self.Multiplexed_Signal_time_Domain.enable_grid(False)
        self.Multiplexed_Signal_time_Domain.enable_axis_labels(True)
        self.Multiplexed_Signal_time_Domain.enable_control_panel(False)
        self.Multiplexed_Signal_time_Domain.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.Multiplexed_Signal_time_Domain.set_line_label(i, "Data {0}".format(i))
            else:
                self.Multiplexed_Signal_time_Domain.set_line_label(i, labels[i])
            self.Multiplexed_Signal_time_Domain.set_line_width(i, widths[i])
            self.Multiplexed_Signal_time_Domain.set_line_color(i, colors[i])
            self.Multiplexed_Signal_time_Domain.set_line_style(i, styles[i])
            self.Multiplexed_Signal_time_Domain.set_line_marker(i, markers[i])
            self.Multiplexed_Signal_time_Domain.set_line_alpha(i, alphas[i])

        self._Multiplexed_Signal_time_Domain_win = sip.wrapinstance(self.Multiplexed_Signal_time_Domain.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._Multiplexed_Signal_time_Domain_win)
        self.InPhase_Carrier = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 10000, 1, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.InPhase_Carrier, 0), (self.blocks_throttle2_2_1_0, 0))
        self.connect((self.Quadrature_Demodulator, 0), (self.low_pass_filter_1, 0))
        self.connect((self.Quadrature_Product_Modulator, 0), (self.multiplexed_signal, 1))
        self.connect((self.blocks_complex_to_real_0_2, 0), (self.Quadrature_Demodulator, 0))
        self.connect((self.blocks_complex_to_real_0_2, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.blocks_complex_to_real_0_2, 0), (self.inphase_Demodulator, 1))
        self.connect((self.blocks_complex_to_real_0_2_0, 0), (self.Quadrature_Demodulator, 1))
        self.connect((self.blocks_complex_to_real_0_3, 0), (self.inphase_Demodulator, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.Multiplexed_Signal_time_Domain, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.blocks_throttle2_1_0, 0), (self.Recovered_Signal_m2_1, 0))
        self.connect((self.blocks_throttle2_1_1, 0), (self.Recovered_Signal_m1_1, 0))
        self.connect((self.blocks_throttle2_2_0, 0), (self.Quadrature_Product_Modulator, 0))
        self.connect((self.blocks_throttle2_2_0, 0), (self.Recovered_Signal_m2, 0))
        self.connect((self.blocks_throttle2_2_1, 0), (self.Recovered_Signal_m1, 0))
        self.connect((self.blocks_throttle2_2_1, 0), (self.inPhase_Product_Modulator, 1))
        self.connect((self.blocks_throttle2_2_1_0, 0), (self.blocks_complex_to_real_0_3, 0))
        self.connect((self.blocks_throttle2_2_1_0, 0), (self.inPhase_Product_Modulator, 0))
        self.connect((self.blocks_throttle2_2_1_0, 0), (self.quadrature_carrier, 0))
        self.connect((self.inPhase_Product_Modulator, 0), (self.multiplexed_signal, 0))
        self.connect((self.inphase_Demodulator, 0), (self.low_pass_filter_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_throttle2_1_1, 0))
        self.connect((self.low_pass_filter_1, 0), (self.blocks_throttle2_1_0, 0))
        self.connect((self.m1, 0), (self.blocks_throttle2_2_1, 0))
        self.connect((self.m2, 0), (self.blocks_throttle2_2_0, 0))
        self.connect((self.multiplexed_signal, 0), (self.blocks_complex_to_real_0_2, 0))
        self.connect((self.quadrature_carrier, 0), (self.Quadrature_Product_Modulator, 1))
        self.connect((self.quadrature_carrier, 0), (self.blocks_complex_to_real_0_2_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "qam_qcm")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.InPhase_Carrier.set_sampling_freq(self.samp_rate)
        self.Multiplexed_Signal_time_Domain.set_samp_rate(self.samp_rate)
        self.Recovered_Signal_m1.set_samp_rate(self.samp_rate)
        self.Recovered_Signal_m1_1.set_samp_rate(self.samp_rate)
        self.Recovered_Signal_m2.set_samp_rate(self.samp_rate)
        self.Recovered_Signal_m2_1.set_samp_rate(self.samp_rate)
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)
        self.blocks_throttle2_1_0.set_sample_rate(self.samp_rate)
        self.blocks_throttle2_1_1.set_sample_rate(self.samp_rate)
        self.blocks_throttle2_2_0.set_sample_rate(self.samp_rate)
        self.blocks_throttle2_2_1.set_sample_rate(self.samp_rate)
        self.blocks_throttle2_2_1_0.set_sample_rate(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 800, 300, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_1.set_taps(firdes.low_pass(1.5, self.samp_rate, 3800, 300, window.WIN_HAMMING, 6.76))
        self.m1.set_sampling_freq(self.samp_rate)
        self.m2.set_sampling_freq(self.samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)




def main(top_block_cls=qam_qcm, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
