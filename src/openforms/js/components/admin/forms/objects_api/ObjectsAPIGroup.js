import {useField, useFormikContext} from 'formik';
import PropTypes from 'prop-types';
import {FormattedMessage} from 'react-intl';
import {useUpdateEffect} from 'react-use';

import Field from 'components/admin/forms/Field';
import FormRow from 'components/admin/forms/FormRow';
import ReactSelect from 'components/admin/forms/ReactSelect';

const ObjectsAPIGroup = ({
  apiGroupChoices,
  onChangeCheck,
  name = 'objectsApiGroup',
  onApiGroupChange,
  isClearable = false,
  required = true,
}) => {
  const [{onChange: onChangeFormik, ...fieldProps}, , {setValue}] = useField(name);
  const {setValues} = useFormikContext();
  const {value} = fieldProps;

  // Call `onApiGroupChange` to get the 'reset' values whenever the API group changes.
  useUpdateEffect(() => {
    if (!onApiGroupChange) return;
    setValues(onApiGroupChange);
  }, [setValues, onApiGroupChange, value]);

  const options = apiGroupChoices.map(([value, label]) => ({value, label}));

  // React doesn't like null/undefined as it leads to uncontrolled component warnings,
  // so we translate null -> '' and vice versa in the change handler
  const normalizedValue = value === null ? '' : value;
  const normalizedOptions = options.map(option => ({
    ...option,
    value: option.value === null ? '' : option.value,
  }));

  return (
    <FormRow>
      <Field
        name={name}
        required={required}
        label={
          <FormattedMessage
            description="Objects API group field label"
            defaultMessage="API group"
          />
        }
        helpText={
          <FormattedMessage
            description="Objects API group field help text"
            defaultMessage="The API group specifies which objects and objecttypes services to use."
          />
        }
        noManageChildProps
      >
        <ReactSelect
          name={name}
          options={normalizedOptions}
          value={normalizedOptions.find(option => option.value === normalizedValue)}
          required={required}
          onChange={selectedOption => {
            const okToProceed = onChangeCheck === undefined || onChangeCheck();
            if (okToProceed) {
              // normalize empty string back to null
              const newValue = selectedOption ? selectedOption.value : null;
              setValue(newValue);
            }
          }}
          isClearable={isClearable}
        />
      </Field>
    </FormRow>
  );
};

ObjectsAPIGroup.propTypes = {
  apiGroupChoices: PropTypes.arrayOf(
    PropTypes.arrayOf(
      PropTypes.oneOfType([
        PropTypes.number, // value
        PropTypes.string, // label
      ])
    )
  ).isRequired,

  /**
   * Optional callback to confirm the change. Return `true` to continue with the change,
   * return `false` to abort it.
   */
  onChangeCheck: PropTypes.func,

  /**
   * Name to use for the form field, is passed down to Formik.
   */
  name: PropTypes.string,

  /**
   * Callback to invoke when the API group value changes, e.g. to reset any dependent fields.
   *
   * The function will be called with Formik's previous values so you can construct a new
   * values state from that.
   *
   * **NOTE**
   *
   * It's best to define this callback at the module level, or make use of `useCallback`
   * to obtain a stable reference to the callback, otherwise the callback will likely
   * fire unexpectedly during re-renders.
   */
  onApiGroupChange: PropTypes.func,

  /**
   * Optional boolean to indicate whether or not it should be possible to clear the
   * select (default `false`)
   */
  isClearable: PropTypes.bool,

  /**
   * Indicate if the field is required or optional.
   */
  required: PropTypes.bool,
};

export default ObjectsAPIGroup;
