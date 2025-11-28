import RadioGroup from '@mui/material/RadioGroup';
import RadioButton from '../../atoms/RadioButton';

function PriorityRadioGroup({ data, defaultValue, name, handleChange, ...props }) {
    return (
        <RadioGroup defaultValue={defaultValue} name={name} onChange={handleChange} {...props}>
            {data.map(item => <RadioButton key={item.id} value={item.id} label={item.label} />)}
        </RadioGroup>
    );
}

export default PriorityRadioGroup;