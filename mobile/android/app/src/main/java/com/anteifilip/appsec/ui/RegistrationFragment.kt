package com.anteifilip.appsec.ui

import android.os.Bundle
import android.view.View
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.navigation.fragment.findNavController
import com.anteifilip.appsec.R
import com.anteifilip.appsec.databinding.FragmentRegistrationBinding
import com.anteifilip.appsec.models.UserRegistrationBody
import com.anteifilip.appsec.utils.onClickDebounced
import com.anteifilip.appsec.utils.viewBinding
import org.koin.androidx.viewmodel.ext.android.viewModel

class RegistrationFragment : Fragment(R.layout.fragment_registration) {

    private val binding by viewBinding(FragmentRegistrationBinding::bind)
    private val viewModel: AppSecViewModel by viewModel()

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        observeViewModel()
        initViews()
    }

    private fun observeViewModel() {
        viewModel.userError.observe(viewLifecycleOwner) {
            Toast.makeText(
                requireContext(),
                "Registration failed. Please try again.",
                Toast.LENGTH_SHORT
            ).show()
        }
        viewModel.userResponse.observe(viewLifecycleOwner) {
            Toast.makeText(
                requireContext(),
                "Registration success. Please log in.",
                Toast.LENGTH_SHORT
            ).show()
            findNavController().navigate(RegistrationFragmentDirections.openLogin())
        }
    }

    private fun initViews() = binding.apply {
        registerButton.onClickDebounced {
            viewModel.user(
                UserRegistrationBody(
                    emailEditText.text.toString(),
                    usernameEditText.text.toString(),
                    passwordEditText.text.toString()
                )
            )
        }
    }
}