package com.anteifilip.appsec.ui

import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.Toast
import androidx.fragment.app.Fragment
import com.anteifilip.appsec.R
import com.anteifilip.appsec.databinding.FragmentLoginBinding
import com.anteifilip.appsec.models.UserBody
import com.anteifilip.appsec.utils.PreferenceHelper
import com.anteifilip.appsec.utils.PreferenceHelper.set
import com.anteifilip.appsec.utils.onClickDebounced
import com.anteifilip.appsec.utils.viewBinding
import org.koin.androidx.viewmodel.ext.android.viewModel

class LoginFragment : Fragment(R.layout.fragment_login) {

    private val binding by viewBinding(FragmentLoginBinding::bind)
    private val viewModel: AppSecViewModel by viewModel()

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        observeViewModel()
        initViews()
    }

    private fun observeViewModel() {
        viewModel.loginError.observe(viewLifecycleOwner) {
            Toast.makeText(
                requireContext(),
                "Login failed. Please try again.",
                Toast.LENGTH_SHORT
            ).show()
        }
        viewModel.loginResponse.observe(viewLifecycleOwner) {
            Toast.makeText(
                requireContext(),
                "Login success.",
                Toast.LENGTH_SHORT
            ).show()
            PreferenceHelper.defaultPrefs(requireContext())["userId"] = it.id
            PreferenceHelper.defaultPrefs(requireContext())["token"] = it.jwt
            val intent = Intent(context, PostsActivity::class.java)
            requireActivity().startActivity(intent)
            requireActivity().overridePendingTransition(
                R.anim.enter_from_right_anim,
                R.anim.exit_to_left_anim
            )
            requireActivity().finish()
        }
    }

    private fun initViews() = binding.apply {
        authButton.onClickDebounced {
            viewModel.login(
                UserBody(
                    usernameEditText.text.toString(),
                    passwordEditText.text.toString()
                )
            )
        }
    }
}