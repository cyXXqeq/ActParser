def fill_data_list(data, inj_processed, act_kind):
    data_list = [data['well'].value]
    data_list += inj_processed[:3]

    if act_kind == 'VDS':
        data_list += [
            data['cycle_count'].value,
            data['process_solution'].value,
            data['clay_powder'].volume,
            data['clay_powder'].concentration,
            data['clay_powder'].mass,
            data['buffer'].value,
            data['wood_flour'].volume,
            data['wood_flour'].concentration,
            data['wood_flour'].mass,
            data['squeeze'].value,
            data['injection_pressure'].value,
            data['squeeze_final'].value
        ]

    elif act_kind == 'RBM':
        data_list += [
            data['process_solution'].value,
            data['rbm'].value1,
            data['rbm'].value2,
            data['rbm'].value3,
            data['squeeze_in_process'].value,
            data['injection_pressure'].value,
            data['squeeze_final'].value
        ]

    elif act_kind == 'HES':
        data_list += [
            data['primary_solution'].value,
            data['neftenol_waste_water'].neftenol,
            data['neftenol_waste_water'].waste_water,
            data['hes'].volume,
            data['hes'].concentration,
            data['injection_pressure'].value,
            data['squeeze_final'].value
        ]

    else:
        raise AttributeError('act_kind must be VDS or HES')

    data_list += inj_processed[3:]

    return data_list
