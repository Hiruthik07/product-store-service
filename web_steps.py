"""Web interface step definitions for behave."""
from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

ID_PREFIX = "product_"


@when('I visit the "Home Page"')
def step_visit_home(context):
    """Open the home page"""
    context.driver.get(context.base_url)


@then('I should see "{message}" in the title')
def step_see_title(context, message):
    """Check the page title"""
    assert message in context.driver.title


@when('I set the "{element_name}" to "{text_string}"')
def step_set_field(context, element_name, text_string):
    """Type text into a field"""
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")
    element = context.driver.find_element(By.ID, element_id)
    element.clear()
    element.send_keys(text_string)


@when('I select "{text}" in the "{element_name}" dropdown')
def step_select_dropdown(context, text, element_name):
    """Choose an option in a dropdown"""
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")
    element = Select(context.driver.find_element(By.ID, element_id))
    element.select_by_visible_text(text)


@then('I should see "{text}" in the "{element_name}" dropdown')
def step_see_dropdown(context, text, element_name):
    """Check the selected option of a dropdown"""
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")
    element = Select(context.driver.find_element(By.ID, element_id))
    assert element.first_selected_option.text == text


@then('the "{element_name}" field should be empty')
def step_field_empty(context, element_name):
    """Check a field is empty"""
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")
    element = context.driver.find_element(By.ID, element_id)
    assert element.get_attribute("value") == ""


@when('I copy the "{element_name}" field')
def step_copy_field(context, element_name):
    """Remember a field value"""
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")
    element = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, element_id))
    )
    context.clipboard = element.get_attribute("value")


@when('I paste the "{element_name}" field')
def step_paste_field(context, element_name):
    """Paste the remembered value into a field"""
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")
    element = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(context.clipboard)


@when('I change "{element_name}" to "{text_string}"')
def step_change_field(context, element_name, text_string):
    """Replace the text in a field"""
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")
    element = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(text_string)


@then('I should see "{text_string}" in the "{element_name}" field')
def step_see_field(context, text_string, element_name):
    """Check the value of a field"""
    element_id = ID_PREFIX + element_name.lower().replace(" ", "_")
    found = WebDriverWait(context.driver, 10).until(
        EC.text_to_be_present_in_element_value((By.ID, element_id), text_string)
    )
    assert found


##################################################################
# Required step definitions for Task 7
##################################################################
@when('I press the "{button}" button')
def step_press_button(context, button):
    """Click a button by its text"""
    element = WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, f"//button[normalize-space()='{button}']")
        )
    )
    element.click()


@then('I should see "{name}" in the results')
def step_verify_text(context, name):
    """Text should be present in the search results"""
    found = WebDriverWait(context.driver, 10).until(
        EC.text_to_be_present_in_element((By.ID, "search_results"), name)
    )
    assert found, f"Expected {name} to be present"


@then('I should not see "{name}" in the results')
def step_verify_text_not_present(context, name):
    """Text should NOT be present in the search results"""
    element = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, "search_results"))
    )
    assert name not in element.text, f"Expected {name} not to be present"


@then('I should see the message "{message}"')
def step_verify_message(context, message):
    """A flash message should be present"""
    found = WebDriverWait(context.driver, 10).until(
        EC.text_to_be_present_in_element((By.ID, "flash_message"), message)
    )
    assert found, f"Expected message {message}"
