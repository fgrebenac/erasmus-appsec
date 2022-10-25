package com.anteifilip.appsec.ui

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.FrameLayout
import android.widget.Toast
import com.anteifilip.appsec.R
import com.anteifilip.appsec.databinding.DialogNewPostBinding
import com.anteifilip.appsec.models.PostBody
import com.anteifilip.appsec.utils.PreferenceHelper
import com.anteifilip.appsec.utils.PreferenceHelper.get
import com.anteifilip.appsec.utils.onClickDebounced
import com.anteifilip.appsec.utils.viewBinding
import com.google.android.material.bottomsheet.BottomSheetBehavior
import com.google.android.material.bottomsheet.BottomSheetDialog
import com.google.android.material.bottomsheet.BottomSheetDialogFragment
import org.koin.androidx.viewmodel.ext.android.viewModel

class NewPostDialogFragment(private val onPostSuccess: () -> Unit) : BottomSheetDialogFragment() {

    private val binding by viewBinding(DialogNewPostBinding::bind)
    private val viewModel: AppSecViewModel by viewModel()

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        dialog?.setOnShowListener { dialog ->
            val layout: FrameLayout? =
                (dialog as BottomSheetDialog).findViewById(com.google.android.material.R.id.design_bottom_sheet)
            layout?.let {
                val behavior = BottomSheetBehavior.from(it)
                behavior.skipCollapsed = true
                behavior.state = BottomSheetBehavior.STATE_EXPANDED
            }
        }
        return inflater.inflate(R.layout.dialog_new_post, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        observeViewModel()
        setViews()
    }

    private fun setViews() = binding.apply {
        addPostButton.onClickDebounced {
            viewModel.post(
                PreferenceHelper.defaultPrefs(requireContext())["userId"],
                PostBody(titleEditText.text.toString(), contentEditText.text.toString())
            )
        }
    }

    private fun observeViewModel() {
        viewModel.postResponse.observe(viewLifecycleOwner) {
            onPostSuccess.invoke()
            dismiss()
        }
        viewModel.postError.observe(viewLifecycleOwner) {
            Toast.makeText(requireContext(), "Adding post failed.", Toast.LENGTH_SHORT).show()
        }
    }
}