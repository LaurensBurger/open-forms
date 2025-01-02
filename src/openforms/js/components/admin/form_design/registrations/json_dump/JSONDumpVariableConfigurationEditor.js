import {useFormikContext} from 'formik';
import PropTypes from 'prop-types';
import React from 'react';
import {FormattedMessage} from 'react-intl';

import Field from 'components/admin/forms/Field';
import FormRow from 'components/admin/forms/FormRow';
import {Checkbox} from 'components/admin/forms/Inputs';

const JSONDumpVariableConfigurationEditor = ({variable}) => {
  const {
    values: {formVariables = []},
    setFieldValue,
  } = useFormikContext();
  const isIncluded = formVariables.includes(variable.key);

  return (
    <FormRow>
      <Field name="includeVariable">
        <Checkbox
          name="includeVariableCheckbox"
          label={
            <FormattedMessage
              description="'Include variable' checkbox label"
              defaultMessage="Include variable"
            />
          }
          helpText={
            <FormattedMessage
              description="'Include variable' checkbox help text"
              defaultMessage="Whether to include this variable in the data to be sent."
            />
          }
          checked={isIncluded}
          onChange={event => {
            const shouldBeIncluded = event.target.checked;
            const newFormVariables = shouldBeIncluded
              ? [...formVariables, variable.key] // add the variable to the array
              : formVariables.filter(key => key !== variable.key); // remove the variable from the array
            setFieldValue('formVariables', newFormVariables);
          }}
        />
      </Field>
    </FormRow>
  );
};

JSONDumpVariableConfigurationEditor.propTypes = {
  variable: PropTypes.shape({
    key: PropTypes.string.isRequired,
  }).isRequired,
};

export default JSONDumpVariableConfigurationEditor;
